
# Dequindre /_de-KWIN-der_/ (n.): A minimalist scheduler. 

Dequindre is built for professionals with the most basic use-cases in mind. You can install and configure your first pipeline in minutes. Dequindre makes it easy to configure, test, and deploy workflows. It also functions as a learning tool for students and professionals without the time or resources to setup the requisite architecture for a full-featured scheduler.

Inspired by the complexity of Airflow, Dequindre is build on three design pillars:

1. The schedule should be human readable and optimizable.  
2. Tasks should fail loudly and clearly.  
3. 80% of the work can be done with the bare-essential features.  

Dequindre offers

* No Python dependencies; no third-party bugs
* Single-container deployment
* Legible source code; fewer than 1000 lines
* Fast, dynamic configuration

# Usage

Dequindre allows dynamic configuration with Python. By example, we may program the process to make tea as  

```usage
>>> from dequindre import Task, DAG, Dequindre
>>>
>>> # define tasks and environments
>>> pour_water = Task('pour_water.py, env='kitchen')
>>> boil_water = Task('boil_water.py', env='microwave')
>>> prep_infuser = Task('prep_infuser.py', env='kitchen')
>>> steep_tea = Task('steep_tea.py', env='kitchen')
>>>
>>> # define runtime dependencies
>>> make_tea = DAG(dependencies={
...    boil_water: {pour_water},
...    steep_tea: {boil_water, prep_infuser}
...})
>>>
>>> # run tasks
>>> dq = Dequindre(dag, check_conda=False)
>>> dq = dq.get_schedules()
defaultdict(<class 'set'>, {
    1: {Task(make_tea.py), Task(prep_infuser.py)},
    2: {Task(boil_water.py)},
    3: {Task(steep_tea.py)}
})
>>> dq.run_tasks()
...
```

`dq.run_tasks()` looks at the priorities and runs `conda run -n ENVIRONMENT python PATH` under the hood.

## Getting Started

Dequindre has two requirements: conda and python.

### Prerequisites

Dequindre relies on [conda >=4.6](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) to run tasks in different environments.  

```conda-version
$ conda --version
conda 4.6.4
```

### Installing

```pip
$ pip install dequindre
```

## Contributing

If you're interested in contributing to Dequindre, [raise an issue](https://github.com/vogt4nick/dequindre/issues), make a pull request to `dev`, and reach out to the author, vogt4nick.

Please read [contributing.md](contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.

### Running the tests

Dequindre's tests are currently written entirely with the `pytest` module. Navigate to the repo's directory on your system and use the `pytest` command. Output should resemble

```pytest
$ pytest
============================= test session starts =============================
platform win32 -- Python 3.6.6, pytest-4.2.1, py-1.7.0, pluggy-0.8.1
rootdir: C:\Users\Nick.Vogt\Projects\repos\dequindre, inifile:
collected 25 items

dequindre\tests\test_DAG.py ...............                              [ 60%]
dequindre\tests\test_Dequindre.py ......                                 [ 84%]
dequindre\tests\test_Task.py ....                                        [100%]

========================== 25 passed in 4.14 seconds ==========================
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/vogt4nick/dequindre/tags).  

## License

This project is licensed under the MIT License - see the [license.md](license.md) file for details.

## Acknowledgements

Thank you, Dynatrace, for facilitating the early development of Dequindre during Innovation Day, February 2019.  