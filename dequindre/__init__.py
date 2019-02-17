# -*- coding: utf-8 -*-
"""Task, DAG, and Dequindre classes

This module defines the Task, DAG, and Dequindre classes. Tasks are intended to
hold task-level data. DAGs are intended to hold relationships between Tasks.
Dequindre schedules Tasks in accordance with the DAG(s).

Design is intended
"""

from collections import defaultdict
from copy import deepcopy
from hashlib import md5
import os
from typing import Dict, Set
from subprocess import run as subprocess_run
from time import sleep


class CyclicGraphError(Exception):
    pass


class Task:
    """Defines a Task and its relevant attributes. Tasks with the same loc
    are equal.

    Tasks are instantiated by three variables: loc, stage, and env.

    Args and Attributes:
        loc (str): location of the python script that runs the task.
        stage (int, >0): Prioritizes tasks. e.g. Tasks with stage 2 run after
            all stage 1 tasks have completed.
        env (str): Which environment to run.
    """
    def __init__(self, loc: str, stage: int, env: str):
        assert isinstance(loc, str), 'loc must be a str'
        assert len(loc) > 0, 'loc cannot be an empty string'
        assert isinstance(stage, int), 'stage must be an int'
        assert stage > 0, 'Stage must be > 0'
        assert isinstance(env, str), 'env must be a str'
        assert len(env) > 0, 'env cannot be an empty string'

        self.loc = loc
        self.stage = stage
        self.env = env

        return None


    def __hash__(self):
        """md5 is fast, and chances of colision are really low"""
        loc = self.loc
        stage = str(self.stage)
        env = self.env
        hash_str = '-'.join((loc, stage, env))
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
        filename = os.path.basename(self.loc)
        return f"{Task.__qualname__}({filename})"


    def __str__(self):
        """Tasks are idenfied by their loc"""
        return repr(self)


class DAG:
    """Defines a directed acyclic graph with tasks and directed edges. Not
    obviously, a DAG may contain more than one graph. Also not obviously,
    new Tasks defined by edges are automatically added to the set of tasks.

    DAGs are instantiated without arguments.

    Attributes:
        tasks (Set[Task]): The set of all tasks. Need not
        edges (Dict[Task, Set[Task]]): A dict of directed edges from one Task
            to a set of Tasks.

    TODO: The DAG should catch cycles before they get to Dequindre.
    TODO: Consider defining edges at instantiation.
    TODO: Define edges as downstream: upstream.
    TODO: Consider renaming "edge" to dependency or something more intuitive
        for users.
    """

    def __init__(self):
        self.tasks = set()
        self.edges = defaultdict(set)
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


    def add_tasks(self, tasks: list):
        """Add multiple tasks to the set of tasks

        TODO: Handle iterables
        TODO: Handle non-iterables
        """
        assert isinstance(tasks, list), TypeError('tasks is not a list')

        for t in tasks:
            self.add_task(t)

        return None


    def remove_task(self, task: Task):
        """Remove task from the set of tasks and remove any related edges

        TODO: Define remove_tasks
        """
        assert isinstance(task, Task), TypeError('task is not a dequindre Task')

        self.tasks.remove(task)

        # remove task from edges
        for k in self.edges:
            if task in self.edges[k]:
                self.edges[k].remove(task)
        if task in self.edges:
            del self.edges[task]

        return None


    def add_edge(self, start: Task, end:Task):
        """Add directed edge to DAG"""
        # error handling by add_tasks won't be clear to the user.
        assert isinstance(start, Task), TypeError('start is not a dequindre Task')
        assert isinstance(end, Task), TypeError('end is not a dequindre Task')

        self.add_tasks([start, end])
        self.edges[start].add(end)

        return None


    def add_edges(self, d: dict):
        """Add directed edges to the DAG"""
        for k, v in d.items():
            if isinstance(v, Task):
                self.add_edge(k, v)
                continue
            elif isinstance(v, set):
                for vi in v:
                    self.add_edge(k, vi)

        return None


    def add_dependency(self, task: Task, depends_on: Task):
        """Add dependency to DAG
        
        Examples:
        >>> dag.add_dependency(steep_tea, depends_on=boil_water)
        """
        # error handling by add_tasks won't be clear to the user.
        assert isinstance(task, Task), TypeError('start is not a dequindre Task')
        assert isinstance(depends_on, Task), TypeError('end is not a dequindre Task')

        self.add_tasks([task, depends_on])
        self.edges[depends_on].add(task)

        # cycles can only be introduced here
        if self.is_cyclic():
            msg = f'Adding the dependency {depends_on} -> {task}' \
                  f'introduced a cycle'
            raise CyclicGraphError(msg)

        return None
    
    
    def add_dependencies(self, d: Dict[Task, Set[Task]]):
        """Add dependencies to DAG
        
        Examples:
        >>> dag.add_dependencies({steep_tea: {boil_water, get_tea_leaves}})
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
            {k: v for k, v in self.edges.items() if len(v) > 0})


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
        activate_env_cmd (str): e.g. ". activate", "source activate"

    Attributes:
        dag (DAG): A copy of the originally supplied DAG. This attribute is
            trimmed while planning the schedule.
        original_dag (DAG): The originally supplied DAG. Used to refresh dag
            after the schedule is planned.

    TODO: The DAG should catch cycles before they get to Dequindre.
    TODO: Define exception for when cycles are detected
    """
    def __init__(self, dag: DAG, activate_env_cmd: str):
        assert isinstance(activate_env_cmd, str), 'activate_env_cmd must be a str'
        assert len(activate_env_cmd) > 0, 'activate_env_cmd must not be an empty str'
        self.activate_env_cmd = activate_env_cmd

        self.original_dag = dag
        self.refresh_dag()

        return None
    

    def __repr__(self):
        return f"{Dequindre.__qualname__}({self.dag})"


    def refresh_dag(self):
        """Create a deepcopy of the original_dag."""
        self.dag = deepcopy(self.original_dag)

        return None


    def get_task_priorities(self, max_stage) -> Dict[Task, int]:
        """Define priority level for each task

        Example:
            make_tea -> pour_tea -> drink_tea will give the dict
            {
                make_tea: 1,
                pour_tea: 2,
                drink_tea: 3
            }
        """
        assert isinstance(max_stage, int), 'max_stage must be an int'
        assert max_stage > 1, 'max_stage must be greater than 1'
        
        dag = self.dag  # copy to something easier to read

        too_high_stage = set([t for t in dag.tasks if t.stage > max_stage])

        for task in too_high_stage:
            dag.remove_task(task)

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


    def get_priorities(self, max_stage) -> Dict[int, Set[Task]]:
        """Define tasks for each priority level.

        Example:
            make_tea -> pour_tea -> drink_tea will give the dict
            {
                1: {make_tea},
                2: {pour_tea},
                3: {drink_tea}
            }
        """
        priorities = defaultdict(set)
        task_priorities = self.get_task_priorities(max_stage=max_stage)
        for k, v in task_priorities.items():
            priorities[v].add(k)

        self.refresh_dag()

        return priorities


    def run_task(self, task: Task):
        """Run the python file defined by Task.loc"""
        assert hash(task) in [hash(t) for t in self.dag.tasks], \
            ValueError(f'{task} is not in the dag')

        r = subprocess_run(
            f'{task.env} {task.loc}',
            shell=True, check=True)

        return None


    def run_tasks(self, max_stage: int = 10000):
        """Run all tasks on the DAG that are less than max_stage"""
        self.refresh_dag()  # refresh just in case
        priorities = self.get_priorities(max_stage=max_stage)

        for k, tasks in priorities.items():
            for task in tasks:
                try:
                    self.run_task(task)
                except Exception as err:
                    print(err)
                sleep(1)
