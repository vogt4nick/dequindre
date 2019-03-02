"""Unit tests for the DAG class."""

import pytest

from dequindre import Task, DAG, CyclicGraphError

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------

def get_two_tasks():
    return (
        Task('A.py', env='test-env'),
        Task('B.py', env='test-env')
    )

# ----------------------------------------------------------------------------
# DAG magic methods
# ----------------------------------------------------------------------------
def test__DAG_init():
    DAG()

    # init with dependencies
    make_tea = Task('make_tea.py', 'test-env')
    drink_tea = Task('drink_tea.py', 'test-env')
    DAG(dependencies={drink_tea: make_tea})


def test__DAG_repr():
    make_tea = Task('make_tea.py', 'test-env')
    dag = DAG()
    dag.add_task(make_tea)
    assert repr(dag) == "DAG({Task(make_tea.py)})"

# ----------------------------------------------------------------------------
# DAG.tasks
# ----------------------------------------------------------------------------
def test__DAG_add_task():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_task(A)

    assert dag.tasks == {A,}, 'Test Task was not added to the DAG'


def test__DAG_add_tasks():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks({A, B})

    assert dag.tasks == {A,B}, 'Test Tasks were not added to the DAG'


def test__DAG_remove_task():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks({A, B})
    dag.remove_task(A)

    assert dag.tasks == {B}, 'Test Task was not added to the DAG'

# ----------------------------------------------------------------------------
# add dependencies
# ----------------------------------------------------------------------------
def test__DAG_add_dependency():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, A)
    assert dag._edges[A] == set([B])


def test__DAG_add_dependency_detect_cycle():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, A)
    with pytest.raises(CyclicGraphError):
        dag.add_dependency(A, B)


def test__DAG_add_dependencies():
    A, B = get_two_tasks()
    C = Task('C.py', env='test-env')
    dag = DAG()
    dag.add_dependencies({B: A})
    assert dag._edges[A] == set([B])

    dag = DAG()
    dag.add_dependencies({C: {A, B}})
    assert dag._edges[A] == set([C])
    assert dag._edges[B] == set([C])


def test__DAG_add_dependency_detect_cycle():
    A, B = get_two_tasks()
    C = Task('C.py', env='test-env')

    dag = DAG()
    with pytest.raises(CyclicGraphError):
        dag.add_dependencies({
            A: C,
            B: A,
            C: B
        })

# ----------------------------------------------------------------------------
# methods
# ----------------------------------------------------------------------------
def test__DAG_get_downstream():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, depends_on=A)
    assert dag.get_downstream() is not None
    assert dag.get_downstream()[A] == {B,}
    assert dag.get_downstream() == {A: {B,}}, 'Task B is not downstream'


def test__DAG_get_upstream():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, depends_on=A)
    assert dag.get_upstream() is not None
    assert dag.get_upstream()[B] == {A,}
    assert dag.get_upstream() == {B: {A,}}, 'Task A is not upstream'


def test__DAG_get_sources():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, depends_on=A)
    assert dag.get_sources() is not None
    assert dag.get_sources() == {A,}


def test__DAG_get_sinks():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, depends_on=A)
    assert dag.get_sinks() is not None
    assert dag.get_sinks() == {B,}


def test__DAG_is_cyclic():
    A, B = get_two_tasks()
    dag = DAG()

    dag.add_dependency(B, depends_on=A)
    assert not dag.is_cyclic(), 'acyclic graph idenfied as cyclic'
    
    with pytest.raises(CyclicGraphError):
        dag.add_dependency(A, depends_on=B)
