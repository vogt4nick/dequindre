"""Unit tests for the Dequindre class."""

from collections import defaultdict

import pytest

from dequindre import Task, DAG, Dequindre


def test__Dequindre_init_exceptions():
    """Raise expected exceptions
    """
    A = Task('A.py', 'test-env')
    B = Task('B.py', 'test-env')
    C = Task('C.py', 'test-env')

    dag = DAG()
    dag.add_tasks({A, B, C})

    with pytest.raises(TypeError):
        Dequindre()

    return None


def test__Dequindre_init():
    """Nothing should break here
    """
    A = Task('A.py', 'test-env')
    B = Task('B.py', 'test-env')
    C = Task('C.py', 'test-env')

    dag = DAG()
    dag.add_tasks({A, B, C})
    dq = Dequindre(dag)

    return None


def test__Dequindre_repr():
    make_tea = Task('make_tea.py', 'test-env')
    dag = DAG()
    dag.add_task(make_tea)
    dq = Dequindre(dag)
    assert repr(dq) == "Dequindre(DAG({Task(make_tea.py)}))"


def test__Dequindre_refresh_dag():
    A = Task('A.py', 'test-env')
    B = Task('B.py', 'test-env')
    C = Task('C.py', 'test-env')
    dag = DAG()
    dag.add_tasks({A, B, C})
    dq = Dequindre(dag)

    tasks = sorted(list(dq.dag.tasks))
    for t in tasks:
        dq.dag.remove_task(t)
    
    assert dq.dag.tasks == set()

    dq.refresh_dag()

    new_tasks = sorted(list(dq.dag.tasks))
    for t, nt in zip(tasks, new_tasks):
        assert t == nt


def test__Dequindre_get_task_schedules():
    A = Task('A.py', 'test-env')
    B = Task('B.py', 'test-env')
    C = Task('C.py', 'test-env')
    Z = Task('Z.py', 'test-env')
    dag = DAG()
    dag.add_tasks({A, B, C, Z})
    dag.add_dependencies({B:A, C:B})
    dq = Dequindre(dag)

    priorities = dq.get_task_schedules()

    testable = {hash(k): v for k, v in priorities.items()}
    assert testable == {
        hash(A): 1, 
        hash(B): 2, 
        hash(C): 3, 
        hash(Z): 1
    }


def test__Dequindre_get_schedules():
    A = Task('A.py', 'test-env')
    B = Task('B.py', 'test-env')
    C = Task('C.py', 'test-env')
    Z = Task('Z.py', 'test-env')
    dag = DAG()
    dag.add_tasks({A, B, C, Z})
    dag.add_dependencies({B:A, C:B})
    dq = Dequindre(dag)

    priorities = dq.get_schedules()
    testable = {}

    # build a testable result dict
    for k, v in priorities.items():
        new_set = set()
        if isinstance(v, Task):
            testable[k] = set(v)
            continue

        for vi in v:
            new_set.add(hash(vi))
        testable[k] = new_set

    assert testable == {
        1: {hash(A), hash(Z)},
        2: {hash(B)}, 
        3: {hash(C)},
    }


# run task(s) tests in test_example.py
