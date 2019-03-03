"""Environment path shortcuts for easier access.

The three main virtual environment modules follow different structures. We 
define three functions to simplify paths to these virtual environments.

- venv_shortcut
- pipenv_shortcut
- conda_shortcut
"""

from os.path import join as pathjoin
from typing import Callable


def venv_shortcut(prefix: str = '.', suffix: str = None) -> Callable:
    """Quickly construct a path to a virtualenv environment

    venv follows the structure: `/path/to/{{my_env}}/Scripts/python`

    Args:
        prefix (str): The file path before the environment name.
        suffix (str, optional): The file path after the environment name.

    Returns:
        Function to shorten env specification
    """
    if suffix is None:
        suffix = pathjoin('Scripts', 'python')
    return lambda s: pathjoin(prefix, s, suffix)


def pipenv_shortcut(prefix: str = '.', suffix: str = None) -> Callable:
    """Quickly construct a path to a pipenv environment

    pipenv follows the structure: `/path/to/{{my_env}}/Scripts/python`

    Args:
        prefix (str): The file path before the environment name.
        suffix (str, optional): The file path after the environment name.

    Returns:
        Function to shorten env specification
    """
    if suffix is None:
        suffix = pathjoin('Scripts', 'python')
    return lambda s: pathjoin(prefix, s, suffix)


def conda_shortcut(prefix: str, suffix: str = None) -> Callable:
    """Quickly construct a path to a conda environment

    conda follows the structure: `/path/to/conda/envs/{{my_env}}/bin/python`

    Args:
        prefix (str): The file path before the environment name.
        suffix (str, optional): The file path after the environment name.

    Returns:
        Function to shorten env specification
    """
    if suffix is None:
        suffix = pathjoin('bin', 'python')
    return lambda s: pathjoin(prefix, s, suffix)

