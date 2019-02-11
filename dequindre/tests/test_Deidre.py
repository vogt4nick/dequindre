
from collections import defaultdict

import pytest

from dequindre import Task, DAG, Dequindre


def get_cyclic_graph():
    A = Task('A.py', stage=1, env='test-env')
    B = Task('B.py', stage=1, env='test-env')
    C = Task('C.py', stage=1, env='test-env')

    dag = DAG()
    dag.add_dedges({A: B, B: C, C: A})

    return dag

def get_breakfast_dag():
    get_cereal = Task('get_cereal.py', 1, env='test-env')
    get_milk = Task('get_milk.py', 1, env='test-env')
    get_bowl = Task('get_bowl.py', 1, env='test-env')
    pour_cereal = Task('pour_cereal.py', 1, env='test-env')
    pour_milk = Task('pour_milk.py', 1, env='test-env')
    eat_breakfast = Task('eat_breakfast.py', 1, env='test-env')

    dag = DAG()
    dag.add_dedges({
        get_cereal: pour_cereal, 
        get_milk: pour_milk, 
        get_bowl: pour_cereal, 
        pour_cereal: pour_milk,
        pour_milk: eat_breakfast,
    })

    return dag

def test__Deidre_init():
    dag = get_cyclic_graph()
    
    with pytest.raises(Exception):
        Dequindre(dag)

    dag = get_breakfast_dag()
    assert isinstance(Dequindre(dag), Dequindre)


def test__Deidre_refresh_dag():
    dag = get_breakfast_dag()
    dd = Dequindre(dag)

    # avoid "set changed size during iteration" error
    tasks = [t for t in dd.dag.tasks]
    for t in tasks:
        dd.dag.remove_task(t)

    assert dd.dag.tasks == set()
    dd.refresh_dag()
    assert dd.dag.tasks != set()


def test__Deidre_get_task_priorities():
    dag = get_breakfast_dag()
    dd = Dequindre(dag)

    tp = dd.get_task_priorities(max_stage=100)
    assert isinstance(tp, defaultdict)
