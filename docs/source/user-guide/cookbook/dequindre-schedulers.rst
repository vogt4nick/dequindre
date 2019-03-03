Dequindre Schedulers
--------------------

The Dequindre scheduler is the last major object in dequindre. After defining 
your tasks and task dependencies in the DAG, you can create a Dequindre 
scheduler.  

.. code-block:: python

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
