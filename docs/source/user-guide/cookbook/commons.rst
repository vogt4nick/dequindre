
Commons
-------

The ``commons`` submodule removes clutter from your config files. Even small 
workflows share many parent directories and environments. To this end,
the ``commons`` submodule makes heavy use of context managers for readability.


Common Tasks
~~~~~~~~~~~~

.. code-block:: python

    >>> from dequindre.commons import common_task

    >>> common_prefix = '/long/path/to/tea-tasks'
    >>> with common_task(common_prefix) as T:
    ...     pour_tea = T(loc='pour_tea.py')
    ...     drink_tea = T(loc='drink_tea.py')
    ... 
    >>> pour_tea
    Task(/long/path/to/tea-tasks/pour_tea.py)
    >>> drink_tea
    Task(/long/path/to/tea-tasks/drink_tea.py)
    >>> pour_tea.env
    'python'
 
The resulting task definitions are much easier to read.

Common Environments
~~~~~~~~~~~~~~~~~~~

Virtual environments get ugly fast, and they're best kept out of sight for 
many users. 

.. code-block:: python

    >>> from dequindre import Task
    >>> from dequindre.commons import common_venv

    >>> common_prefix = '/my/very/long/path'
    >>> with common_venv(common_prefix) as E:
    ...     tea_env = E('tea-env')
    ...     biscuit_env = E('biscuit-env')
    ... 
    >>> tea_env
    '/my/very/long/path/tea-env/bin/python'
    >>> drink_tea = Task('./drink_tea.py', tea_env)
    >>> drink_tea.env
    '/my/very/long/path/tea-env/bin/python'

Notice that ``common_venv`` filled in the expected suffix: ``/bin/python``. 
You can override this behavior with the ``common_suffix`` argument.

The same functionality is also supported for pipenv environments and conda 
environments through the ``common_pipenv`` and ``common_conda_env`` functions
respectively.
