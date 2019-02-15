#!/usr/bin/env python3

import os
from os.path import join as pathjoin

from dequindre import Task, DAG, Dequindre


def demo():
    # init tasks
    # CONDA_ENV_DIR = os.environ['CONDA_DIR']
    python27_env = pathjoin('~', '..', 'opt', 'conda', 'envs', 'python27', 'bin', 'python')
    python35_env = pathjoin('~', '..', 'opt', 'conda', 'envs', 'python35', 'bin', 'python')
    python36_env = pathjoin('~', '..', 'opt', 'conda', 'envs', 'python36', 'bin', 'python')
    python37_env = pathjoin('~', '..', 'opt', 'conda', 'envs', 'python37', 'bin', 'python')

    # DEQUINDRE_DIR = os.environ['DEQUINDRE_DIR']
    python27 = Task(pathjoin('~', '..', 'opt', 'dequindre-demo', 'tasks', 'run_python27.py'), stage=1, env=python27_env)
    python35 = Task(pathjoin('~', '..', 'opt', 'dequindre-demo', 'tasks', 'run_python35.py'), stage=1, env=python35_env)
    python36 = Task(pathjoin('~', '..', 'opt', 'dequindre-demo', 'tasks', 'run_python36.py'), stage=1, env=python36_env)
    python37 = Task(pathjoin('~', '..', 'opt', 'dequindre-demo', 'tasks', 'run_python37.py'), stage=1, env=python37_env)

    # construct DAG from tasks
    dag = DAG()
    dag.add_dependencies({
        python35: python27,
        python36: {python27, python35},
        python37: {python27, python35, python36},
    })

    # init Dequindre with DAG
    dq = Dequindre(dag, activate_env_cmd='doesnt matter')
    dq.run_tasks()

    return None


if __name__ == '__main__':
    demo()
