
Task Environments
~~~~~~~~~~~~~~~~~

virtualenv Environments
^^^^^^^^^^^^^^^^^^^^^^^

Suppose you want to run tasks in a different virtualenv environment. Let's 
define a virtualenv environment:

.. code-block:: bash

    $ virtualenv venv
    ...

virtualenv envirionments have a defined structure. The path to the python 
executable is `./venv/Scripts/python`. This will become our task env.

.. code-block:: python

    >>> from dequindre import Task
    >>> venv = './venv/Scripts/python'
    >>> pour_tea = Task('./pour_tea.py', env=venv)
    >>> pour_tea.env
    './venv/Scripts/python'

Now the task will run in the specified environment at runtime.

pipenv Environments
^^^^^^^^^^^^^^^^^^^

pipenv environments follow the same structure as virtualenv environments. They
may be be located elsewhere on you file system. Finding it is easy. Note that 
you may have to delete your recently created `venv` directory.

.. code-block:: bash

    $ pipenv install dequindre
    ...
    $ pipenv shell
    Launching subshell in virtual environment
    $ where python
    /your/path/to/.virtualenvs/dequindre-5srOTnbr/Scripts/python

The output will be different on your machine, and there may be multiple paths,
but the pipenv path will include the `.virtualenvs/` directory.

.. code-block:: python

    >>> from dequindre import Task
    >>> from os.path import join as pathjoin
    >>> PIPENV_DIR = '/path/to/your/.virtualenvs'

    >>> dequindre_env = pathjoin(PIPENV_DIR, 'dequindre-5srOTnbr', 
                                 'Scripts', 'python')
    >>> pour_tea = Task('./pour_tea.py', env=dequindre_env)
    >>> pour_tea.env
    '/your/path/to/.virtualenvs/dequindre-5srOTnbr/Scripts/python'

Now the task is pointing to the pipenv environment and will run that 
environment at runtime.

conda Environments
^^^^^^^^^^^^^^^^^^

Suppose you want to run tasks using your conda environments. Conda 
environments are slightly trickier than virtualenv environments.

First, create a test environment and find where your conda installation is 
located. You'll ought to see something like

.. code-block:: bash

    $ conda create -n test_env python=3.6
    ...
    $ where conda
    /your/path/to/miniconda3/condabin/
    /your/path/to/miniconda3/Scripts/conda
    /your/path/to/miniconda3/Library/bin/conda

The output will be different on your machine, but the important directory is
the common directory; in this case, it's miniconda3.

conda, like virtualenv and pipenv, also has a well defined structure for 
environments that looks like `miniconda3/envs/test_env/bin/python`.

.. code-block:: python

    >>> from dequindre import Task
    >>> from os.path import join as pathjoin
    >>> CONDA_DIR = '/your/path/to/miniconda3'

    >>> test_env = pathjoin(CONDA_DIR, 'envs', 'test_env', 'bin', 'python')
    >>> pour_tea = Task('./pour_tea.py', env=venv)
    >>> pour_tea.env
    '/your/path/to/miniconda3/envs/test_env/Scripts/python'

Now the task is pointing to the conda environment and will run that 
environment at runtime.
