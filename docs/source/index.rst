Dequindre /\_de-KWIN-der\_/ (n.): A minimalist scheduler.
=======================================================

.. toctree::
   :maxdepth: 2

   license
   help

Quick Start
^^^^^^^^^^^

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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
