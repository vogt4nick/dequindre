Design
======

Class Structure
---------------

There are three classes in dequindre, they are

-  ``Task``,
-  ``DAG``, and
-  ``Dequindre``.

You’ll notice that dequindre rarely abstracts information. This goes
hand in hand with the principle that tasks should fail loudly and
clearly. Dequindre is stripped of many high-level features to facilitate
a shallow learning curve.

Task
~~~~

``Task``\ s are the atomic elements of dequindre. They contain two
pieces of information:

1. ``loc`` is the path to the target python script.
2. ``env`` the name of the pre-defined runtime environment.

DAG
~~~

``DAG`` is short for directed acyclic graph. ``DAG``\ s have two
attributes and a host of methods to easily navigate task dependencies.
The methods are:

-  ``add_task(task)`` and ``add_tasks(tasks)`` allows you to add tasks
   to the DAG without defining dependencies. The former accepts a Task
   input, the latter accepts a set of Tasks.
-  ``remove_task(task)`` removes a specific task.
-  ``add_dependency(task, depends_on)`` lets you define a dependency
   between two tasks. If you haven’t added one of the tasks via
   ``add_task``, the task will be automatically added to the DAG along
   with the dependency.
-  ``add_dependencies(d)`` lets you define several dependencies at once.
   It accepts a dict of key-value pairs like ``Task: Set[Task]``. Single
   task values don’t have to be passed as a set.
-  ``get_downstream()`` and ``get_upstream()`` return the adjacency dict
   of downstream or upstream tasks.
-  ``get_sources()`` and ``get_sinks()`` return the set of tasks with no
   upstream and no downstream dependencies respectively.
-  ``is_cyclic()`` returns a boolean if the DAG contains any cyclic
   depdendencies.

It’s best not to access the attributes directly unless you know what
you’re doing. The two attributes are:

1. ``tasks`` is the set of all tasks known to the DAG.
2. ``_edges`` is an adjacency dict of directed edges from one Task to a
   set of Tasks.

Not obviously, a DAG may contain more than one graph. Also not
obviously, new Tasks defined by edges are automatically added to the set
of tasks. DAGs are instantiated without arguments.

Dequindre
~~~~~~~~~

Dequinder is the scheduler; it looks at the DAG and runs each task in
order. As before, it’s best to leverage the methods instead of the
attributes. The methods are:

-  ``get_task_schedules()`` returns a dict of task-int key-value pairs.
   The value determines when the task will run. 1 runs first, 2 runs
   second, and so on.

   -  e.g. The dependencies ``make_tea -> pour_tea -> drink_tea`` will
      give the dict ``{make_tea: 1, pour_tea: 2, drink_tea: 3}``

-  ``get_schedules()`` returns the reverse: a dict of int-task key-value
   pairs.

   -  e.g. The dependencies ``make_tea -> pour_tea -> drink_tea`` will
      give the dict ``{1: {make_tea}, 2: {pour_tea}, 3: {drink_tea}}``

-  ``run_task(task)`` and ``run_tasks()`` allow you to run a specific
   task independent of the dag or every task according to the schedule.