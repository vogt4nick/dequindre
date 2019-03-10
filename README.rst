============================================================
Dequindre /de-KWIN-der/ (n.): A minimalist workflow manager.
============================================================

.. image:: https://img.shields.io/pypi/pyversions/dequindre.svg
    :alt: Supported Versions
    :target: https://pypi.org/project/dequindre/

.. image:: https://img.shields.io/readthedocs/dequindre.svg
    :alt: Documentation
    :target: https://dequindre.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/v/dequindre.svg?color=blue
    :alt: Version
    :target: https://pypi.org/project/dequindre/

.. .. image:: https://img.shields.io/github/last-commit/vogt4nick/dequindre.svg
..     :alt: Last Commit
..     :target: https://github.com/vogt4nick/dequindre

.. image:: https://img.shields.io/github/license/vogt4nick/dequindre.svg
    :alt: License
    :target: https://github.com/vogt4nick/dequindre

.. image:: https://img.shields.io/pypi/dw/dequindre.svg
    :alt: PyPI - Downloads
    :target: https://pypi.org/project/dequindre/

.. .. image:: https://img.shields.io/github/issues/vogt4nick/dequindre.svg
..     :alt: Count Open Issues
..     :target: https://pypi.org/project/dequindre/

Dequindre Is Easy to Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~
Anywhere Python goes, Dequindre can follow. Dequindre is written in pure 
python and is OS independent. All you need is to ``pip install dequindre``.

Dequindre Is Easy to Run
~~~~~~~~~~~~~~~~~~~~~~~~
Dequindre makes it easy to run virtual environments. Dequindre supports 
virtualenv, pipenv, and conda environments.

Dequindre Is Easy to Learn
~~~~~~~~~~~~~~~~~~~~~~~~~~
You can run your first Dequindre workflow in minutes. Dequindre is less
than 1000 lines of Python and `fully documented`_. In contrast, `Airflow
v1.10.2 has 444 pages of docs`_.

.. _`fully documented`: https://dequindre.readthedocs.io/en/stable/
.. _`Airflow v1.10.2 has 444 pages of docs`:
  https://media.readthedocs.org/pdf/airflow/1.10.2/airflow.pdf


Your First Dequindre Schedule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Install dequindre from PyPI ``pip install dequindre``. Then in the REPL,

.. code-block:: python

    >>> from dequindre import Task, DAG, Dequindre

    >>> ## define tasks and environments
    >>> boil_water = Task('./boil_water.py')
    >>> steep_tea = Task('./steep_tea.py')
    >>> drink_tea = Task('./drink_tea.py')

    >>> ## define runtime dependencies
    >>> make_tea = DAG(dependencies={
    ...     steep_tea: boil_water,
    ...     drink_tea: steep_tea
    ... })

    >>> ## create schedules
    >>> dq = Dequindre(make_tea)
    >>> dq.get_schedules()
    defaultdict(<class 'set'>, {
        1: {Task(./boil_water.py)},
        2: {Task(./steep_tea.py)},
        3: {Task(./drink_tea.py)}})

    >>> ## run tasks if the files exist.
    >>> dq.run_tasks()
    Running Task(./boil_water.py)

    I am boiling water...

    Running Task(./steep_tea.py)

    I am steeping tea...

    Running Task(./drink_tea.py)

    I am drinking tea...

You can run the tasks by copy-pasting the following python code into the
commented files.

.. code-block:: python

    # pour_water.py
    print("I'm pouring water...")


.. code-block:: python

    # boil_water.py
    print("I'm boiling water...")


.. code-block:: python

    # steep_tea.py
    print("I'm steeping tea...")


Features
~~~~~~~~

- **Automated workflow scheduling**
- **Pure Python**: Relies entirely on Python built-ins to reduce bugs and 
  complexity
- **Cross-Python compatible**: Supports Python 2 and Python 3
- **Cross-platform**: Windows and Unix style OS environments
- **Run your Python tasks in any pre-defined environments**
    - dequindre facilitates **virtualenv**, **conda**, and **pipenv** 
      environments
- **Supports dynamic workflow configuration** also seen in Airflow
- **Documented** examples and configuration

Extras
~~~~~~

License
^^^^^^^

This project is licensed under the MIT License - see the LICENSE_ file for details.

.. _LICENSE: https://github.com/vogt4nick/dequindre/blob/master/LICENSE


Versioning
^^^^^^^^^^

We use SemVer_ for versioning. For the versions available, see the `tags on this repository`_.

.. _SemVer: http://semver.org/
.. _tags on this repository: https://github.com/vogt4nick/dequindre/tags


Contribute
^^^^^^^^^^

If you're interested in contributing to Dequindre, `raise an issue`_, make a
pull request to `dev`, and reach out to the author, vogt4nick.

.. _raise an issue: https://github.com/vogt4nick/dequindre/issues

Please read `our contribution guidelines`_ for details on our code of conduct,
and the process for submitting pull requests to us.

.. _our contribution guidelines: https://github.com/vogt4nick/dequindre/blob/master/CONTRIBUTE.rst


Acknowledgements
^^^^^^^^^^^^^^^^

Thank you, Dynatrace, for facilitating the early development of Dequindre
during Innovation Day, February 2019.
