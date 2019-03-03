# -*- coding: utf-8 -*-
"""Task, DAG, and Dequindre classes

This module defines the Task, DAG, and Dequindre classes. Tasks are intended to
hold task-level data. DAGs are intended to hold relationships between Tasks.
Dequindre schedules Tasks in accordance with the DAG.
"""

from collections import defaultdict
from copy import deepcopy
from hashlib import md5
import os
from typing import Dict, Set
from subprocess import run as subprocess_run
from subprocess import check_output, CalledProcessError


__version__ = '0.8.5'


class CyclicGraphError(Exception):
    pass


class Task:
    """Define a Task and its relevant attributes. 
    
    Note:
        Tasks with the same loc and env are equal.

    Attributes:
        loc (str): location of the python script that runs the task.
        env (str, optional): Which environment to run.
    """
    def __init__(self, loc: str, env: str = 'python'):
        """Init a Task.

        Args:
            loc (str): location of the python script that runs the task.
            env (str, optional): Which environment to run.
        """
        assert isinstance(loc, str), 'loc must be a str'
        assert len(loc) > 0, 'loc cannot be an empty string'
        assert isinstance(env, str), 'env must be a str'
        assert len(env) > 0, 'env cannot be an empty string'

        self.loc = loc
        self.env = env

        return None


    def __hash__(self):
        """md5 is fast, and chances of colision are really low"""
        loc = self.loc
        env = self.env
        hash_str = '-'.join((loc, env))
        big_int = int(md5(hash_str.encode()).hexdigest(), 16)

        return big_int


    def __eq__(self, other: 'Task') -> bool:
        if not isinstance(other, type(self)):
            return False
        return hash(self) == hash(other)


    def __lt__(self, other: 'Task') -> bool:
        """Tasks are otherwise sorted by their loc"""
        return self.loc < other.loc


    def __repr__(self):
        """Tasks are idenfied by their loc"""
        return f"{Task.__qualname__}({self.loc})"


    def __str__(self):
        """Tasks are idenfied by their loc"""
        return repr(self)


class DAG:
    """Define a DAG and relationships between tasks. 
    
    A DAG is a directed acyclic graph with tasks and dependencies as nodes
    and directed edges respectively. You have the option to define all the 
    tasks and dependencies at once if you prefer that syntax.

    Note:
        Not obviously, a DAG may contain more than one graph. Also not 
        obviously, new Tasks defined by edges are automatically added to the
        set of tasks.

    Attributes:
        tasks (`set` of `Task`): The set of all tasks. Dequindre will try to 
            run every task in this attribute.
        _edges (`dict` of `Task`: `set` of `Task`): A dict of directed edges 
            from one Task to a set of Tasks. Access directly at your own peril.
    """

    def __init__(self, *, tasks: set = None, dependencies: dict = None):
        """Init a DAG.

        Args:
            tasks (`set` of `Task`): Add Tasks to the DAG.
            dependencies (`dict` of `Task`: `set` of `Task`): Add dependencies
                to the DAG.
        """
        self.tasks = set()
        self._edges = defaultdict(set)

        if tasks is not None:
            assert isinstance(tasks, set), '`tasks` must be a set of tasks'
            self.add_tasks(tasks)

        if dependencies is not None:
            assert isinstance(dependencies, dict), '`dependencies` must be a dict'
            self.add_dependencies(dependencies)

        return None


    def __repr__(self):
        if self.tasks:
            return f"""{DAG.__qualname__}({repr(self.tasks)})"""
        return f"{DAG.__qualname__}({set()})"

    # ------------------------------------------------------------------------
    # Config DAG
    # ------------------------------------------------------------------------

    def add_task(self, task: Task) -> None:
        """Add a task to the set of tasks
        
        Args:
            task (`Task`): A Task object.
        """
        assert isinstance(task, Task), TypeError('task is not a Task')
        self.tasks.add(task)

        return None


    def add_tasks(self, tasks: set) -> None:
        """Add multiple tasks to the set of tasks.
        
        Args:
            tasks (`set` of `Task`): Tasks to be added to the DAG.
        """
        assert isinstance(tasks, (set, Task)), TypeError('tasks is not a set')

        if isinstance(tasks, Task):
            task = tasks
            self.add_task(task)

            return None

        for t in tasks:
            self.add_task(t)

        return None


    def remove_task(self, task: Task) -> None:
        """Remove task from the set of tasks and remove any related edges

        Args:
            task (`Task`): A task to be removed from the DAG.
        """
        assert isinstance(task, Task), TypeError('task is not a dequindre Task')

        self.tasks.remove(task)

        # remove task from edges
        for k in self._edges:
            if task in self._edges[k]:
                self._edges[k].remove(task)
        if task in self._edges:
            del self._edges[task]

        return None


    def remove_tasks(self, tasks: set) -> None:
        """Remove multiple tasks from the set of tasks and any related edges
        
        Args:
            tasks (`set` of `Task`): Tasks to be removed from the DAG.
        """
        assert isinstance(tasks, (set, Task)), TypeError('tasks is not a set')

        if isinstance(tasks, Task):
            task = tasks
            self.remove_task(task)

            return None

        for t in tasks:
            self.remove_task(t)

        return None

    def add_dependency(self, task: Task, depends_on: Task) -> None:
        """Add dependency to DAG.

        Args:
            task (`Task`): The downstream task.
            depends_on (`Task`): The upstream task.

        Note:
            If either task does not yet exist in DAG, the task will 
            automatically be added to the dag.

        Examples:
            >>> from dequindre import Task, DAG
            >>> boil_water = Task('boil_water.py')
            >>> steep_tea = Task('steep_tea.py')
            >>> dag = DAG()
            >>> dag.add_dependency(steep_tea, depends_on=boil_water)
        """
        # error handling by add_tasks won't be clear to the user.
        assert isinstance(task, Task), TypeError('start is not a dequindre Task')
        assert isinstance(depends_on, Task), TypeError('end is not a dequindre Task')

        self.add_tasks({task, depends_on})
        self._edges[depends_on].add(task)

        # cycles can only be introduced here
        if self.is_cyclic():
            msg = f'Adding the dependency {depends_on} -> {task}' \
                  f'introduced a cycle'
            raise CyclicGraphError(msg)

        return None


    def add_dependencies(self, d: Dict[Task, Set[Task]]) -> None:
        """Add multiple dependencies to DAG

        Args:
            d (`dict` of `Task`: `set` of `Task`): An adjacency dict mapping
                downstream Tasks to possibly many upstream tasks.

        Note:
            If any tasks do not yet exist in DAG, the task will automatically 
            be added to the dag.

        Examples:
            >>> from dequindre import Task, DAG
            >>> boil_water = Task('boil_water.py')
            >>> prep_infuser = Task('prep_infuser.py')
            >>> steep_tea = Task('steep_tea.py')
            >>> dag = DAG()
            >>> dag.add_dependencies({steep_tea: {boil_water, prep_infuser}})
        """
        for task, dependencies in d.items():
            if isinstance(dependencies, Task):
                dependency = dependencies
                self.add_dependency(task, dependency)
                continue
            elif isinstance(dependencies, set):
                for dependency in dependencies:
                    self.add_dependency(task, dependency)

    # ------------------------------------------------------------------------
    # Graph Utilities
    # ------------------------------------------------------------------------
    # nested loops are easier to read here. If time-complexity becomes a 
    # problem, the user clearly needs to use a full-featured scheduler

    def get_downstream(self) -> dict:
        """Return adjacency dict of downstream Tasks.
        
        Returns:
            `dict` of `Task`: `set` of `Task`
        """
        return defaultdict(set,
            {k: v for k, v in self._edges.items() if len(v) > 0})


    def get_upstream(self) -> dict:
        """Return adjacency dict of upstream Tasks
        
        Returns:
            `dict` of `Task`: `set` of `Task`
        """
        upstream = defaultdict(set)
        for u, d in self.get_downstream().items():
            for v in d:
                upstream[v].add(u)

        return upstream


    def get_sources(self) -> set:
        """Return the set of source Tasks (Tasks with no upstream dependencies)

        Returns:
            `set` of `Task`
        """
        sources = set()
        for t in self.tasks:
            if t in self.get_upstream():
                continue
            sources.add(t)

        return sources


    def get_sinks(self) -> set:
        """Return the set of sink Tasks (Tasks with no downstream dependencies)

        Returns:
            `set` of `Task`
        """
        sinks = set()
        for t in self.tasks:
            if t in self.get_downstream():
                continue
            sinks.add(t)

        return sinks


    def _is_cyclic(self, task, visited, stack) -> bool:
        """Helper function for is_cyclic
        
        Returns:
            True if cycle detected. False otherwise.
        """
        visited[task] = True
        stack[task] = True

        for d in self.get_downstream()[task]:
            if not visited[d]:
                if self._is_cyclic(d, visited, stack):
                    return True
            elif stack[d]:
                return True

        stack[task] = False

        return False


    def is_cyclic(self) -> bool:
        """Detect if the DAG is cyclic.
        
        Returns:
            True if cycle detected. False otherwise.
        """
        ## developers note:
        ## I used this source as reference, but the algorithm is pretty well
        ## documented everywhere
        ## https://www.geeksforgeeks.org/detect-cycle-in-a-graph/

        visited = {t: False for t in self.tasks}
        # which tasks are in recursion stack
        stack = {t: False for t in self.tasks}
        for task in self.tasks:
            if not visited[task]:
                if self._is_cyclic(task, visited, stack):
                    return True
        return False


class Dequindre:
    """The Dequindre scheduler handles all the scheduling computations.

    Attributes:
        dag (DAG): A copy of the originally supplied DAG. This attribute is
            trimmed while planning the schedule.
        original_dag (DAG): The originally supplied DAG. Used to refresh dag
            after the schedule is planned.
    """
    def __init__(self, dag: DAG):
        """Init a Dequindre scheduler.

        Args:
            dag (DAG): A DAG of tasks and dependencies to be scheduled.
        """
        self.original_dag = dag
        self.refresh_dag()

        return None


    def __repr__(self):
        return f"{Dequindre.__qualname__}({self.dag})"


    def refresh_dag(self) -> None:
        """Create a deepcopy of the original_dag."""
        self.dag = deepcopy(self.original_dag)

        return None


    def get_task_schedules(self) -> Dict[Task, int]:
        """Define schedule priority level for each task

        Returns:
            `dict` of `Task`: `int`

        Example:
            make_tea -> pour_tea -> drink_tea will give the dict
            {
                make_tea: 1,
                pour_tea: 2,
                drink_tea: 3
            }
        """
        dag = self.dag  # copy to something easier to read
        task_priority = defaultdict(int)
        visited = set()
        i = 1

        while dag.get_sources():
            task_priority.update({t: i for t in dag.get_sources()})
            for t in dag.get_sources():
                visited.add(t)
                dag.remove_task(t)
            i += 1

        self.refresh_dag()

        return task_priority


    def get_schedules(self) -> Dict[int, Set[Task]]:
        """Schedule tasks by priority level.

        Returns:
            `dict` of `int`: `set` of `Task`

        For example, make_tea -> pour_tea -> drink_tea will give the dict
            {1: {make_tea},
             2: {pour_tea},
             3: {drink_tea}}
        """
        priorities = defaultdict(set)
        task_priorities = self.get_task_schedules()
        for k, v in task_priorities.items():
            priorities[v].add(k)

        self.refresh_dag()

        return priorities


    def run_task(self, task: Task) -> None:
        """Run the python file defined by Task.loc in the environment defined 
        by the Task.env
        
        Args:
            task (`Task`): The task to be run.
        """
        assert hash(task) in [hash(t) for t in self.dag.tasks], \
            ValueError(f'{task} is not in the dag')

        print(f'\nRunning {repr(task)}\n', flush=True)
        r = subprocess_run(f'{task.env} {task.loc}', shell=True, check=True)

        return None


    def run_tasks(self) -> None:
        """Run all tasks on the DAG"""
        self.refresh_dag()  # refresh just in case
        priorities = self.get_schedules()

        for k, tasks in priorities.items():
            for task in tasks:
                try:
                    self.run_task(task)
                except Exception as err:
                    print(err, flush=True)
