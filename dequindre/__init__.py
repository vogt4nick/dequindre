# -*- coding: utf-8 -*-
"""Task, DAG, and Dequindre classes

This module defines the Task, DAG, and Dequindre classes. Tasks are intended to
hold task-level data. DAGs are intended to hold relationships between Tasks.
Dequindre schedules Tasks in accordance with the DAG(s).
"""

from collections import defaultdict
from copy import deepcopy
from hashlib import md5
import os
from typing import Dict, Set
from subprocess import run as subprocess_run
from subprocess import check_output, CalledProcessError


__version__ = '0.7.0.dev0'


class CyclicGraphError(Exception):
    pass
class Task:
    """Defines a Task and its relevant attributes. Tasks with the same loc
    are equal.

    Tasks are instantiated by three variables: loc, and env.

    Args and Attributes:
        loc (str): location of the python script that runs the task.
        env (str): Which environment to run.
    """
    def __init__(self, loc: str, env: str = 'base'):
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
    """Defines a directed acyclic graph with tasks and dependencies as nodes
    and directed edges respectively.

    Not obviously, a DAG may contain more than one graph. Also not obviously,
    new Tasks defined by edges are automatically added to the set of tasks.

    Instantiation:
        DAG(tasks: Set[Task], dependencies: Dict[Task, Set[Task]]) -> None:
            You have the option to define all the tasks and dependencies at
            once if you prefer that syntax.

    Attributes:
        tasks (Set[Task]):
            The set of all tasks. Dequindre will try to run every task in
            this attribute.
        _edges (Dict[Task, Set[Task]]):
            A dict of directed edges from one Task to a set of Tasks. Access
            directly at your own peril.

    Methods:
        add_task(task: Task) -> None:
            Add one task to the DAG with no dependencies.
        add_tasks(tasks: Set[Task]) -> None:
            Add multiple tasks to the DAG with no dependencies.
        remove_task(task: Task) -> None:
            Remove one task from the DAG. This also removes all dependencies
            downstream and upstream of the task.
        remove_tasks(tasks: Set[Task]) -> None:
            Remove multiple tasks from the DAG with no dependencies. This also
            removes all dependencies downstream and upstream of the task.
        add_dependency(task: Task, depends_on: Task) -> None:
            Add a task dependency to the DAG. If either task does not yet
            exist in DAG, the task will automatically be added to the dag.
        add_dependencies(d: Dict[Task, Set[Task]]) -> None:
            Add multiple task dependencies to the DAG. If any task does not
            yet exist in DAG, the task will automatically be added to the
            dag.
        get_downstream() -> (Dict[Task, Set[Task]]):
            Get the adjacency dict of downstream Tasks.
        get_upstream() -> (Dict[Task, Set[Task]]):
            Get the adjacency dict of upstream Tasks.
        get_sources() -> (Set(Task)):
            Get the set of all tasks with no upstream dependencies.
        get_sinks() -> (Set[Task]):
            Get the set of all tasks with no downstream dependencies.
    """

    def __init__(self, *, tasks: set = None, dependencies: dict = None):
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

    def add_task(self, task: Task):
        """Add a task to the set of tasks"""
        assert isinstance(task, Task), TypeError('task is not a Task')
        self.tasks.add(task)

        return None


    def add_tasks(self, tasks: set):
        """Add multiple tasks to the set of tasks

        TODO: Handle iterables
        TODO: Handle non-iterables
        """
        assert isinstance(tasks, set), TypeError('tasks is not a set')

        for t in tasks:
            self.add_task(t)

        return None


    def remove_task(self, task: Task):
        """Remove task from the set of tasks and remove any related edges
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


    def remove_tasks(self, tasks: set):
        """Remove multiple tasks from the set of tasks

        TODO: Handle iterables
        TODO: Handle non-iterables
        """
        assert isinstance(tasks, (set, Task)), TypeError('tasks is not a set')

        if isinstance(tasks, Task):
            task = tasks
            self.remove_task(task)

            return None

        for t in tasks:
            self.remove_task(t)

        return None

    def add_dependency(self, task: Task, depends_on: Task):
        """Add dependency to DAG

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


    def add_dependencies(self, d: Dict[Task, Set[Task]]):
        """Add dependencies to DAG

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
    def get_downstream(self) -> dict:
        """Return adjacency dict of downstream Tasks."""
        return defaultdict(set,
            {k: v for k, v in self._edges.items() if len(v) > 0})


    def get_upstream(self) -> dict:
        """Return adjacency dict of upstream Tasks"""
        upstream = defaultdict(set)
        for u, d in self.get_downstream().items():
            for v in d:
                upstream[v].add(u)

        return upstream


    def get_sources(self) -> set:
        """Return the set of source Tasks (Tasks with no upstream dependencies)
        """
        sources = set()
        for t in self.tasks:
            if t in self.get_upstream():
                continue
            sources.add(t)

        return sources


    def get_sinks(self) -> set:
        """Return the set of sink Tasks (Tasks with no downstream dependencies)
        """
        sinks = set()
        for t in self.tasks:
            if t in self.get_downstream():
                continue
            sinks.add(t)

        return sinks


    def _is_cyclic(self, task, visited, stack) -> bool:
        """Helper function for is_cyclic"""
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

        Used this source as reference, but the algorithm is pretty well
        documented everywhere
        https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
        """
        visited = {t: False for t in self.tasks}
        # which tasks are in recursion stack
        stack = {t: False for t in self.tasks}
        for task in self.tasks:
            if not visited[task]:
                if self._is_cyclic(task, visited, stack):
                    return True
        return False


class Dequindre:
    """Defines the Dequindre scheduler. She handles all the scheduling
    computations.

    Dequindre is instantiated with a DAG.

    Arguments:
        dag (DAG): A DAG of tasks to be scheduled.

    Attributes:
        dag (DAG): A copy of the originally supplied DAG. This attribute is
            trimmed while planning the schedule.
        original_dag (DAG): The originally supplied DAG. Used to refresh dag
            after the schedule is planned.

    TODO: The DAG should catch cycles before they get to Dequindre.
    TODO: Define exception for when cycles are detected
    """
    def __init__(self, dag: DAG):
        self.original_dag = dag
        self.refresh_dag()

        return None


    def __repr__(self):
        return f"{Dequindre.__qualname__}({self.dag})"


    def refresh_dag(self):
        """Create a deepcopy of the original_dag."""
        self.dag = deepcopy(self.original_dag)

        return None


    def get_task_schedules(self) -> Dict[Task, int]:
        """Define schedule priority level for each task

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


    def run_task(self, task: Task):
        """Run the python file defined by Task.loc"""
        assert hash(task) in [hash(t) for t in self.dag.tasks], \
            ValueError(f'{task} is not in the dag')

        print(f'\nRunning {repr(task)}\n')
        r = subprocess_run(f'{task.env} {task.loc}', shell=True, check=True)

        return None


    def run_tasks(self):
        """Run all tasks on the DAG"""
        self.refresh_dag()  # refresh just in case
        priorities = self.get_schedules()

        for k, tasks in priorities.items():
            for task in tasks:
                try:
                    self.run_task(task)
                except Exception as err:
                    print(err)
