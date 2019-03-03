Dequindre /de-KWIN-der/ (n.): A minimalist scheduler.
=====================================================

.. image:: https://img.shields.io/pypi/pyversions/dequindre.svg
    :alt: Supported Versions
    :target: https://pypi.org/project/dequindre/

.. image:: https://img.shields.io/readthedocs/dequindre.svg
    :alt: Documentation
    :target: https://dequindre.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/v/dequindre.svg?color=blue
    :alt: Version
    :target: https://pypi.org/project/dequindre/

.. image:: https://img.shields.io/github/last-commit/vogt4nick/dequindre.svg
    :alt: Last Commit
    :target: https://github.com/vogt4nick/dequindre

.. image:: https://img.shields.io/github/license/vogt4nick/dequindre.svg
    :alt: License
    :target: https://github.com/vogt4nick/dequindre

.. .. image:: https://img.shields.io/pypi/dw/dequindre.svg
..     :alt: PyPI - Downloads
..     :target: https://pypi.org/project/dequindre/

.. .. image:: https://img.shields.io/github/issues/vogt4nick/dequindre.svg
..     :alt: Count Open Issues
..     :target: https://pypi.org/project/dequindre/


Vision: Simplify Workflow Automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``dequindre`` aims to simplify workflow automation. It is part of a larger 
vision to teach the fundamentals and best practices to practicing and aspiring
data scientists and data engineers.


What is dequindre?
^^^^^^^^^^^^^^^^^^

``dequindre`` is a minimalist scheduler you can use to:

- quickly configure python workflows at home or at work,
- run dependent tasks in separate python environments, and
- learn the fundamentals and best practices of scheduling workflows.


Features
^^^^^^^^

- **Automated workflow scheduling**
- **Pure Python**: Relies entirely on Python built-ins.  
  - This reduces bugs, complexity, and prevents dependency hell.  
- **Cross-Python compatible**: Supports Python 2 and Python 3
- **Cross-platform**: Windows and Unix style OS environments
- **Run your Python tasks in any pre-defined environments**
  - `dequindre` facilitates **virtualenv**, **conda**, and **pipenv** environments
- **Supports dynamic workflow configuration** also seen in Airflow
- **Documented** examples and configuration

Basic Example
^^^^^^^^^^^^^

First, install ``dequindre`` with ``pip install dequindre``. Then, in the REPL or in a ``schedule.py`` file,  

.. code-block :: python

    >>> from dequindre import Task, DAG, Dequindre

    >>> ## define tasks and environments
    >>> pour_water = Task('./tea-tasks/pour_water.py')
    >>> boil_water = Task('./tea-tasks/boil_water.py')
    >>> prep_infuser = Task('./tea-tasks/prep_infuser.py')
    >>> steep_tea = Task('./tea-tasks/steep_tea.py')

    >>> ## define runtime dependencies
    >>> make_tea = DAG(dependencies={
    ...     boil_water: {pour_water},
    ...     steep_tea: {boil_water, prep_infuser}
    ... })

    >>> ## run tasks
    >>> dq = Dequindre(make_tea)
    >>> dq.get_schedules()
    defaultdict(<class 'set'>, {
        1: {Task(prep_infuser.py), Task(pour_water.py)},  
        2: {Task(boil_water.py)},  
        3: {Task(steep_tea.py)}})

    >>> ## dq.run_tasks() can run the files if they exist. 


User Guide
^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   user-guide/intro
   user-guide/design
   user-guide/cookbook
