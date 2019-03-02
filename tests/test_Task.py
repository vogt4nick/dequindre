"""Unit tests for the Task class."""

import pytest

from dequindre import Task


def test__Task_init():
    good_loc = 'path/to/file.py'
    good_env = 'test-env'

    with pytest.raises(TypeError):
        Task()

    with pytest.raises(AssertionError):
        Task(loc=None, env=good_env)

    with pytest.raises(AssertionError):
        Task(loc='', env=good_env)

    with pytest.raises(AssertionError):
        Task(loc=good_loc, env=None)

    Task(loc=good_loc)
    Task(loc=good_loc, env=good_env)


def test__Task_repr():
    make_tea = Task('make_tea.py', 'test-env')
    assert repr(make_tea) == "Task(make_tea.py)"


def test__Task_hash():
    A = Task('test.py', 'test-env')
    B = Task('test.py', 'test-env')

    assert hash(A) == hash(B)

    A.loc = 'new-test.py'

    assert hash(A) != hash(B)


def test__Task_eq():
    A = Task('test.py', 'test-env')
    B = Task('test.py', 'test-env')

    assert A == B

    A.loc = 'new-test.py'

    assert A != B
