
# Cookbook

## Quick Start


```quick-start
>>> from dequindre import Task, DAG, Dequindre
>>>
>>> ## define tasks and environments
>>> pour_water = Task('pour_water.py)
>>> boil_water = Task('boil_water.py')
>>> prep_infuser = Task('prep_infuser.py)
>>> steep_tea = Task('steep_tea.py')
>>>
>>> ## define runtime dependencies
>>> make_tea = DAG(dependencies={
...    boil_water: {pour_water},
...    steep_tea: {boil_water, prep_infuser}
... })
>>>
>>> ## run tasks
>>> dq = Dequindre(make_tea, validate_conda=False)
>>> dq.get_schedules()
defaultdict(<class 'set'>, {
    1: {Task(prep_infuser.py), Task(pour_water.py)},  
    2: {Task(boil_water.py)},  
    3: {Task(steep_tea.py)}})
>>> dq.run_tasks()
```

## Configure Tasks

## Configure DAG

## Run Tasks


## Class Structure

There are three classes in dequindre, they are

- `Task`,  
- `DAG`, and  
- `Dequindre`.

You'll notice that dequindre rarely abstracts information. This goes hand in hand with the principle that tasks should fail loudly and clearly. Dequindre is stripped of many high-level features to facilitate a shallow learning curve.  

### Task

`Task`s are the atomic elements of dequindre. They contain two pieces of information:

1. `loc (str)`: the location of the python script that runs the task.
1. `env (str)`: the name of the runtime environment.

### DAG

DAG is short for directed acyclic graph.  

Not obviously, a DAG may contain more than one graph. Also not obviously, new Tasks defined by edges are automatically added to the set of tasks. DAGs are instantiated without arguments.

DAGS have two attributes and a host of methods to make navigating it easier.

tasks (Set[Task]): The set of all tasks. Need not
edges (Dict[Task, Set[Task]]): A dict of directed edges from one Task to a set of Tasks.

### Dequindre

Dequinder is the scheduler; it looks at the DAG and runs task