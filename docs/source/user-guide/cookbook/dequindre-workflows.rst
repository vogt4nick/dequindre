Dequindre Workflows
-------------------

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


Error Handling
~~~~~~~~~~~~~~

By default, Dequindre uses soft error handling; if one task fails, Dequindre 
assumes it's a non-critical error and continues on. But we don't always want 
this behavior. Instead, if one task fails, we want the whole schedule to fail.

``Dequindre.run_tasks()`` has an optional ``error_handling`` method that takes
one of two values: ``error_handling='soft'`` or ``error_handling='hard'``. The
latter will raise an ``EarlyAbortError`` if any of the tasks fail. 
