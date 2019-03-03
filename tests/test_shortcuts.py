
from os.path import join as pathjoin

import pytest

from dequindre.shortcuts import venv_shortcut
from dequindre.shortcuts import pipenv_shortcut
from dequindre.shortcuts import conda_shortcut


def test__venv_shortcut():
    prefix = pathjoin('path', 'to')
    vc = venv_shortcut(prefix)

    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'Scripts', 'python')
    returned_path = vc(env_name)

    assert returned_path == correct_path


def test__pipenv_shortcut():
    prefix = pathjoin('path', 'to')
    pc = venv_shortcut(prefix)

    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'Scripts', 'python')
    returned_path = pc(env_name)

    assert returned_path == correct_path


def test__conda_shortcut():
    prefix = pathjoin('path', 'to')
    cc = conda_shortcut(prefix)

    env_name = 'my-test-env'
    correct_path = pathjoin(prefix, env_name, 'bin', 'python')
    returned_path = cc(env_name)

    assert returned_path == correct_path

