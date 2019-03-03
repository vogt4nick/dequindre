
import pytest

from dequindre import common_task
from dequindre import Task, DAG, Dequindre


def test__common_task_exceptions():
    with pytest.raises(AssertionError):
        common_task('/path/to/env')

    with pytest.raises(AssertionError):
        common_task('')

    with pytest.raises(AssertionError):
        common_task('/path/to/env/{}', '')

    with pytest.raises(AssertionError):
        common_task('/path/to/env/{}', None)


def test__common_task():
    CommonTask = common_task('./tea-tasks/{}', 'python')
    boil_water = CommonTask('boil_water.py')
    assert isinstance(boil_water, Task)
