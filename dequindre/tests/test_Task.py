
import pytest

from dequindre import Task


def test__Task_init():
    good_loc = 'path/to/file.py'
    good_stage = 1
    good_env = 'test-env'

    assert isinstance(
        Task(loc=good_loc, stage=good_stage, env=good_env),
        Task
    )
    with pytest.raises(AssertionError):
        Task(loc=None, stage=good_stage, env=good_env)

    with pytest.raises(AssertionError):
        Task(loc='', stage=good_stage, env=good_env)

    with pytest.raises(AssertionError):
        Task(loc=good_loc, stage=None, env=good_env)

    with pytest.raises(AssertionError):
        Task(loc=good_loc, stage='prod', env=good_env)

    with pytest.raises(AssertionError):
        Task(loc=good_loc, stage=0, env=good_env)

    with pytest.raises(AssertionError):
        Task(loc=good_loc, stage=good_stage, env=None)

    with pytest.raises(AssertionError):
        Task(loc=good_loc, stage=good_stage, env='')
