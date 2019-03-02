
# Dequindre /\_de-KWIN-der\_/ (n.): A minimalist scheduler.

[![Supported
Versions](https://img.shields.io/pypi/pyversions/dequindre.svg)](https://pypi.org/project/dequindre/)
[![Documentation](https://img.shields.io/readthedocs/dequindre.svg)](https://dequindre.readthedocs.io/en/latest/)
[![Version](https://img.shields.io/pypi/v/dequindre.svg?color=blue)](https://pypi.org/project/dequindre/)
[![Last
Commit](https://img.shields.io/github/last-commit/vogt4nick/dequindre.svg)](https://github.com/vogt4nick/dequindre)
[![License](https://img.shields.io/pypi/l/dequindre.svg?color=red)](https://pypi.org/project/dequindre/)

## Vision

`dequindre` aims to empower workflow automation for everyone. It's part
of a larger vision to teach the fundamentals and best practices to
practicing and aspiring data scientists and data engineers.

## What is dequindre?

`dequindre` is a minimalist scheduler you can use to:

- quickly configure python workflows at home or at work,
- run dependent tasks in separate python environments, and
- learn the fundamentals and best practices of scheduling workflows.

## Basic Example

First, install `dequindre` with `pip install dequindre`. Then, in the
REPL or in a `schedule.py` file,

```basic-example
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
```
## Features

- **Automated workflow scheduling**
- **Run your Python tasks in any pre-defined environments**
  - `dequindre` facilitates **virtualenv** and **conda** environments
- **Supports dynamic workflow configuration** also seen in Airflow
- **Cross-Python compatible**: Supports Python 2 and Python 3
- **Cross-platform**: Windows and Unix style environments
- **Documented** examples and configuration

## Getting Started

Dequindre is has two requirements: conda and python.

### Installing

```pip
$ pip install dequindre
```

## Contributing

If you're interested in contributing to Dequindre, [raise an issue](https://github.com/vogt4nick/dequindre/issues), make a pull request to `dev`, and reach out to the author, vogt4nick.

Please read [contributing.md](contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/vogt4nick/dequindre/tags).  

## License

This project is licensed under the MIT License - see the [license.md](license.md) file for details.

## Acknowledgements

Thank you, Dynatrace, for facilitating the early development of Dequindre during Innovation Day, February 2019.  