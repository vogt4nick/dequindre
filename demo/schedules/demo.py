#!/usr/bin/env python3

from os.path import join as pathjoin

from dequindre import Task, DAG, Dequindre

def demo(homedir: str, activate_env_cmd: str):
    # init tasks
    python27 = Task(pathjoin(homedir, 'run_python27.py'), stage=1, env='python27')
    python35 = Task(pathjoin(homedir, 'run_python35.py'), stage=1, env='python35')
    python36 = Task(pathjoin(homedir, 'run_python36.py'), stage=1, env='python36')
    python37 = Task(pathjoin(homedir, 'run_python37.py'), stage=1, env='python37')   

    # construct DAG from tasks
    dag = DAG()
    dag.add_dedges({
        python27: python35,
        python35: python36,
        python36: python37
    })

    # init Dequindre with DAG
    dd = Dequindre(dag, activate_env_cmd=activate_env_cmd)
    dd.run_tasks()

    return None


if __name__ == '__main__':
    print('Run in ascending order')
    demo(homedir='.\\demo\\tasks', activate_env_cmd='activate')
    # demo(homedir='opt/demo/tasks', activate_env_cmd='. activate')
