Tasks
-----

Configure a Task
~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from dequindre import Task
    >>> pour_tea = Task('./pour_tea.py')
    >>> pour_tea
    Task(./pour_tea.py)
    >>> pour_tea.loc
    './pour_tea.py'
    >>> pour_tea.env
    'python'

Note that that the python environment defaulted to 'python'. To use different 
environments, we'll need to define them first.
