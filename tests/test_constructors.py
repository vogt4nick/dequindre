
from os.path import join as pathjoin

import pytest

from dequindre.constructors import venv_constructor
from dequindre.constructors import pipenv_constructor
from dequindre.constructors import conda_constructor


def test__venv_constructor():
    prefix = pathjoin('path', 'to')
    vc = venv_constructor(prefix)

    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'Scripts', 'python')
    returned_path = vc(env_name)

    assert returned_path == correct_path


def test__pipenv_constructor():
    prefix = pathjoin('path', 'to')
    pc = venv_constructor(prefix)

    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'Scripts', 'python')
    returned_path = pc(env_name)

    assert returned_path == correct_path


def test__conda_constructor():
    prefix = pathjoin('path', 'to')
    cc = conda_constructor(prefix)

    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'bin', 'python')
    returned_path = cc(env_name)

    assert returned_path == correct_path

