
# Cookbook

This cookbook will make use of three sample python files.

```boil_water.py
## ./boil_water.py
print("I am boiling water...")
```

```steep_tea.py
## ./steep_tea.py
print("I am steeping tea...")
```

```pour_tea.py
## ./pour_tea.py
print("I am pouring tea...)
```

We also use Git Bash as the terminal. Bash commands work on windows and unix machines unless otherwise stated.

## Tasks

### Configure a Task

```config-tasks-1
>>> from dequindre import Task
>>> pour_tea = Task('./pour_tea.py')
>>> pour_tea
Task(./pour_tea.py)
>>> pour_tea.loc
'./pour_tea.py'
>>> pour_tea.env
'python'
```

Note that that the python environment defaulted to 'python'. To use different environments, we'll need to define them first.

### Create Tasks in virtualenv Environments

Suppose you want to run tasks in a different virtualenv environment. Let's define a virtualenv environment:

```venv
$ virtualenv venv
...
```

virtualenv envirionments have a defined structure. The path to the python executable is `./venv/Scripts/python`. This will become our task env.

```virtualenv-task
>>> from dequindre import Task
>>> venv = './venv/Scripts/python'
>>> pour_tea = Task('./pour_tea.py', env=venv)
>>> pour_tea.env
'./venv/Scripts/python'
```

Now the task will run in the specified environment at runtime.

### Create Tasks in pipenv Environments

pipenv environments follow the same structure as virtualenv environments. They may be be located elsewhere on you file system. Finding it is easy. Note that you may have to delete your recently created `venv` directory.

```pipenv
$ pipenv install dequindre
...
$ pipenv shell
Launching subshell in virtual environment
$ where python
/your/path/to/.virtualenvs/dequindre-5srOTnbr/Scripts/python
```

The output will be different on your machine, and there may be multiple paths, but the pipenv path will include the `.virtualenvs/` directory.

```pipenv-task
>>> from dequindre import Task
>>> from os.path import join as pathjoin
>>> PIPENV_DIR = '/c/Users/Me/.virtualenvs'

>>> dequindre_env = pathjoin(PIPENV_DIR, 'dequindre-5srOTnbr', 'Scripts', 'python')
>>> pour_tea = Task('./pour_tea.py', env=dequindre_env)
>>> pour_tea.env
'/your/path/to/.virtualenvs/dequindre-5srOTnbr/Scripts/python'
```

Now the task is pointing to the pipenv environment and will run that environment at runtime.

### Create Tasks in conda Environments

Suppose you want to run tasks in a different virtualenv environment. Conda environments are slightly trickier than virtualenv environments.

First, create a test environment and find where your conda installation is located.

```conda
$ conda create -n test_env python=3.6
...
$ where conda
/your/path/to/miniconda3/condabin/
/your/path/to/miniconda3/Scripts/conda
/your/path/to/miniconda3/Library/bin/conda
```

The output will be different on your machine, but the important directory is the common directory; in this case, it's miniconda3.

conda, like virtualenv and pipenv, also has a well defined structure for environments that looks like `miniconda3/envs/test_env/python`.

```conda-task
>>> from dequindre import Task
>>> from os.path import join as pathjoin
>>> CONDA_DIR = '/your/path/to/miniconda3'

>>> test_env = pathjoin(CONDA_DIR, 'envs', 'test_env', 'python')
>>> pour_tea = Task('./pour_tea.py', env=venv)
>>> pour_tea.env
'/your/path/to/miniconda3/envs/test_env/Scripts/python'
```

Now the task is pointing to the conda environment and will run that environment at runtime.

## DAGs

### Configure a DAG

```config-dag
>>> from dequindre import Task, DAG

>>> ## define tasks
>>> boil_water = Task('./boil_water.py')
>>> steep_tea = Task('./steep_tea.py')
>>> pour_tea = Task('./pour_tea.py')

>>> make_tea = DAG()
>>> make_tea.add_dependencies({
...       steep_tea: boil_water,
...       pour_tea: steep_tea
...   })
```

## Dequindre Schedulers

```config-dequindre
>>> from dequindre import Task, DAG, Dequindre

>>> ## define tasks
>>> boil_water = Task('./boil_water.py')
>>> steep_tea = Task('./steep_tea.py')
>>> pour_tea = Task('./pour_tea.py')

>>> make_tea = DAG()
>>> make_tea.add_dependencies({
...       steep_tea: boil_water,
...       pour_tea: steep_tea
...   })

>>> dq = Dequindre(make_tea)
>>> dq.get_schedules()
defaultdict(<class 'set'>, {
    1: {Task(boil_water.py)},  
    2: {Task(steep_tea.py)},  
    3: {Task(pour_tea.py)}})
>>> dq.run_tasks()

Running Task(./boil_water.py)

I am boiling water...

Running Task(./steep_tea.py)

I am steeping tea...

Running Task(./pour_tea.py)

I am pouring tea...
```

## Error Handling
