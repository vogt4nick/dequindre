"""Environment path shortcuts for easier access.

The three main virtual environment modules follow different structures. We 
define three functions to simplify paths to these virtual environments.

- venv_shortcut
- pipenv_shortcut
- conda_shortcut
"""

from contextlib import contextmanager
from os.path import join as pathjoin
from typing import Callable

from dequindre import Task


@contextmanager
def common_task(common_loc: str, common_env: str = 'python'):
    """Create tasks with a common parent path and environment.
    
    Lots of tasks will use the same environment or same directory. These 
    `commons` reduce duplicate code.

    Args:
        common_loc (str): {}-formatted parent path.
        common_env (str, optional): environment.
    """
    assert isinstance(common_loc, str), '`common_loc` must be a str'
    assert len(common_loc) > 0, '`common_loc` must not be an empty str'
    assert '{' in common_loc and '}' in common_loc
    assert isinstance(common_env, str)
    assert len(common_env) > 0, '`common_env` must not be an empty str'

    def construct_task(loc: str):
        return Task(common_loc.format(loc), env=common_env)
    
    yield construct_task


@contextmanager
def common_venv(common_prefix: str = '.', 
                common_suffix: str = None) \
                -> Callable:
    """Quickly construct a path to a common virtualenv environment

    venv follows the structure: `/path/to/{{my_env}}/Scripts/python`

    Args:
        common_prefix (str): The file path before the environment name.
        common_suffix (str, optional): The file path after the environment name.

    Returns:
        Function to shorten env specification
    """
    if common_suffix is None:
        common_suffix = pathjoin('Scripts', 'python')
    yield lambda s: pathjoin(common_prefix, s, common_suffix)


@contextmanager
def common_pipenv(common_prefix: str = '.', 
                  common_suffix: str = None) \
                  -> Callable:
    """Quickly construct a path to a common pipenv environment

    pipenv follows the structure: `/path/to/{{my_env}}/Scripts/python`

    Args:
        common_prefix (str): The file path before the environment name.
        common_suffix (str, optional): The file path after the environment name.

    Returns:
        Function to shorten env specification
    """
    if common_suffix is None:
        common_suffix = pathjoin('Scripts', 'python')
    yield lambda s: pathjoin(common_prefix, s, common_suffix)


@contextmanager
def common_conda_env(common_prefix: str, 
                     common_suffix: str = None) \
                     -> Callable:
    """Quickly construct a path to a common conda environment

    conda follows the structure: `/path/to/conda/envs/{{my_env}}/bin/python`

    Args:
        common_prefix (str): The file path before the environment name.
        common_suffix (str, optional): The file path after the environment name.

    Returns:
        Function to shorten env specification
    """
    if common_suffix is None:
        common_suffix = pathjoin('bin', 'python')
    yield lambda s: pathjoin(common_prefix, s, common_suffix)

