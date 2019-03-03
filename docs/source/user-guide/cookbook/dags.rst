DAGs
----

Configure a DAG
~~~~~~~~~~~~~~~

.. code-block:: python

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

