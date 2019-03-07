
from os.path import join as pathjoin

import pytest

from dequindre import Task, DAG, Dequindre
from dequindre.commons import (
    common_task, common_venv, common_pipenv, common_conda_env
)


def test__common_task_exceptions():
    with pytest.raises(AssertionError):
        with common_task('/path/to/env') as TestTask:
            test_task = TestTask('test')

    with pytest.raises(AssertionError):
        with common_task('') as TestTask:
            test_task = TestTask('test')

    with pytest.raises(AssertionError):
        with common_task('/path/to/env/{}', '') as TestTask:
            test_task = TestTask('test')            

    with pytest.raises(AssertionError):
        with common_task('/path/to/env/{}', None) as TestTask:
            test_task = TestTask('test')


def test__common_task():
    with common_task('./tea-tasks/{}', 'python') as TeaTask:
        boil_water = TeaTask('boil_water.py')
    
    assert isinstance(boil_water, Task)


def test__common_venv():
    prefix = pathjoin('path', 'to')
    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'Scripts', 'python')

    with common_venv(prefix) as venv:
        returned_path = venv(env_name)

    assert returned_path == correct_path


def test__common_pipenv():
    prefix = pathjoin('path', 'to')
    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'Scripts', 'python')

    with common_pipenv(prefix) as pipenv:
        returned_path = pipenv(env_name)

    assert returned_path == correct_path


def test__conda_shortcut():
    prefix = pathjoin('path', 'to')
    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'bin', 'python')
    
    with common_conda_env(prefix) as conda_env:
        returned_path = conda_env(env_name)

    assert returned_path == correct_path
