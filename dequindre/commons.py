# -*- coding: utf-8 -*-
"""Shortcuts to defining tasks and environments.

It's not uncommon for tasks to share a similar parent directory or structure.
Likewise, environments almost always share the same parent directory or
structure. The commons module makes well-founded assumptions about these
structures to improve readability.
"""

from contextlib import contextmanager
from os.path import join as pathjoin
from typing import Callable

from dequindre import Task


@contextmanager
def common_task(loc_pattern: str, common_env: str = 'python'):
    """Create tasks with a common parent path and environment.

    Lots of tasks will use the same environment or same directory. These
    `commons` reduce duplicate code.

    Args:
        loc_pattern (str): {}-formatted parent path.
        common_env (str, optional): environment.

    Example:
        >>> from dequindre.commons import common_task
        >>> with common_task('./tea-tasks/{}/main.py') as T:
        ...     boil_water = T('boil_water')
        ...     steep_tea  = T('steep_tea')
        ...     drink_tea  = T('drink_tea')
        >>> boil_water
        Task(./tea-tasks/boil_water/main.py)
    """
    assert isinstance(loc_pattern, str), '`loc_pattern` must be a str'
    assert loc_pattern, '`loc_pattern` must not be an empty str'
    assert '{' in loc_pattern and '}' in loc_pattern
    assert isinstance(common_env, str)
    assert common_env, '`common_env` must not be an empty str'

    def construct_task(loc: str):
        return Task(loc_pattern.format(loc), env=common_env)

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

    Example:
        >>> #doctest: +SKIP
        >>> from dequindre.commons import common_venv
        >>> with common_venv('./tea-envs') as env:
        ...     python27 = env('python27')
        ...     python36 = env('python36')
        ...
        >>> python27
        './tea-envs/python27/Scripts/python'
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

    Example:
        >>> #doctest: +SKIP
        >>> from dequindre.commons import common_pipenv
        >>> with common_pipenv('/path/to/tea-envs') as env:
        ...     python27 = env('python27')
        ...     python36 = env('python36')
        ...
        >>> python27
        '/path/to/tea-envs/python27/Scripts/python'
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

    Example:
        >>> #doctest: +SKIP
        >>> from dequindre.commons import common_conda_env
        >>> with common_conda_env('/path/to/conda/envs') as env:
        ...     python27 = env('python27')
        ...     python36 = env('python36')
        ...
        >>> python27
        '/path/to/conda/envs/python27/bin/python'
    """
    if common_suffix is None:
        common_suffix = pathjoin('bin', 'python')
    yield lambda s: pathjoin(common_prefix, s, common_suffix)
