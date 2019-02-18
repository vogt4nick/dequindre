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


def get_cyclic_graph():
    A = Task('A.py', env='test-env')
    B = Task('B.py', env='test-env')
    C = Task('C.py', env='test-env')

    dag = DAG()
    dag.add_edges({
        A: B,
        B: C,
        C: A,
    })

    return dag

# ----------------------------------------------------------------------------
# DAG magic methods
# ----------------------------------------------------------------------------
@pytest.mark.run(order=2)
def test__DAG_init():
    assert isinstance(DAG(), DAG), 'DAG init failed'


def test__DAG_repr():
    make_tea = Task('make_tea.py', 'test-env')
    dag = DAG()
    dag.add_task(make_tea)
    assert repr(dag) == "DAG({Task(make_tea.py)})"

# ----------------------------------------------------------------------------
# DAG.tasks
# ----------------------------------------------------------------------------
@pytest.mark.run(order=2)
def test__DAG_add_task():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_task(A)

    assert dag.tasks == {A,}, 'Test Task was not added to the DAG'


@pytest.mark.run(order=2)
def test__DAG_add_tasks():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks({A, B})

    assert dag.tasks == {A,B}, 'Test Tasks were not added to the DAG'


@pytest.mark.run(order=2)
def test__DAG_remove_task():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks({A, B})
    dag.remove_task(A)

    assert dag.tasks == {B}, 'Test Task was not added to the DAG'

# ----------------------------------------------------------------------------
# DAG.edges
# ----------------------------------------------------------------------------
@pytest.mark.run(order=2)
def test__DAG_add_edge():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks({A, B})
    dag.add_edge(A, B)
    assert dag.edges == {A: {B,}}, 'edge was not created'

    del dag 
    dag = DAG()
    dag.add_edge(A, B)
    assert dag.edges == {A: {B,}}, 'edge Tasks were not added to DAG.tasks'


@pytest.mark.run(order=2)
def test__DAG_edges():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_edges({A: B})
    assert isinstance(dag.edges[A], set), 'edge dict value is not a set'

# ----------------------------------------------------------------------------
# add dependencies
# ----------------------------------------------------------------------------
def test__DAG_add_dependency():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dependency(B, A)
    assert dag.edges[A] == set([B])


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
    assert dag.edges[A] == set([B])

    dag = DAG()
    dag.add_dependencies({C: {A, B}})
    assert dag.edges[A] == set([C])
    assert dag.edges[B] == set([C])


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
@pytest.mark.run(order=2)
def test__DAG_get_downstream():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_edge(A, B)
    assert dag.get_downstream() is not None
    assert dag.get_downstream()[A] == {B,}
    assert dag.get_downstream() == {A: {B,}}, 'Task B is not downstream'


@pytest.mark.run(order=2)
def test__DAG_get_upstream():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_edge(A, B)
    assert dag.get_upstream() is not None
    assert dag.get_upstream()[B] == {A,}
    assert dag.get_upstream() == {B: {A,}}, 'Task A is not upstream'


@pytest.mark.run(order=2)
def test__DAG_get_sources():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_edge(A, B)
    assert dag.get_sources() is not None
    assert dag.get_sources() == {A,}


@pytest.mark.run(order=2)
def test__DAG_get_sinks():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_edge(A, B)
    assert dag.get_sinks() is not None
    assert dag.get_sinks() == {B,}


@pytest.mark.run(order=2)
def test__DAG_is_cyclic():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_edge(A, B)
    assert not dag.is_cyclic(), 'acyclic graph idenfied as cyclic'
    
    dag = get_cyclic_graph()
    assert dag.is_cyclic(), 'cyclic graph idenfied as acyclic'
