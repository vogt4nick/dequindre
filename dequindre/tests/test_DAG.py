"""Unit tests for the DAG class."""

import pytest

from dequindre import Task, DAG

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------

@pytest.mark.run(order=2)
def get_two_tasks():
    return (
        Task('A.py', stage=1, env='test-env'),
        Task('B.py', stage=1, env='test-env')
    )


@pytest.mark.run(order=2)
def get_cyclic_graph():
    A = Task('A.py', stage=1, env='test-env')
    B = Task('B.py', stage=1, env='test-env')
    C = Task('C.py', stage=1, env='test-env')

    dag = DAG()
    dag.add_dedges({
        A: B,
        B: C,
        C: A,
    })

    return dag

# ----------------------------------------------------------------------------
# DAG.__init__
# ----------------------------------------------------------------------------
@pytest.mark.run(order=2)
def test__DAG_init():
    assert isinstance(DAG(), DAG), 'DAG init failed'

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
    dag.add_tasks([A, B])

    assert dag.tasks == {A,B}, 'Test Tasks were not added to the DAG'


@pytest.mark.run(order=2)
def test__DAG_remove_task():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks([A, B])
    dag.remove_task(A)

    assert dag.tasks == {B}, 'Test Task was not added to the DAG'

# ----------------------------------------------------------------------------
# DAG.dedges
# ----------------------------------------------------------------------------
@pytest.mark.run(order=2)
def test__DAG_add_dedge():
    A, B = get_two_tasks()

    dag = DAG()
    dag.add_tasks([A, B])
    dag.add_dedge(A, B)
    assert dag.dedges == {A: {B,}}, 'dedge was not created'

    del dag 
    dag = DAG()
    dag.add_dedge(A, B)
    assert dag.dedges == {A: {B,}}, 'dedge Tasks were not added to DAG.tasks'


@pytest.mark.run(order=2)
def test__DAG_dedges():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dedges({A: B})
    assert isinstance(dag.dedges[A], set), 'dedge dict value is not a set'

# ----------------------------------------------------------------------------
# methods
# ----------------------------------------------------------------------------
@pytest.mark.run(order=2)
def test__DAG_get_downstream():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dedge(A, B)
    assert dag.get_downstream() is not None
    assert dag.get_downstream()[A] == {B,}
    assert dag.get_downstream() == {A: {B,}}, 'Task B is not downstream'


@pytest.mark.run(order=2)
def test__DAG_get_upstream():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dedge(A, B)
    assert dag.get_upstream() is not None
    assert dag.get_upstream()[B] == {A,}
    assert dag.get_upstream() == {B: {A,}}, 'Task A is not upstream'


@pytest.mark.run(order=2)
def test__DAG_get_sources():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dedge(A, B)
    assert dag.get_sources() is not None
    assert dag.get_sources() == {A,}


@pytest.mark.run(order=2)
def test__DAG_get_sinks():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dedge(A, B)
    assert dag.get_sinks() is not None
    assert dag.get_sinks() == {B,}


@pytest.mark.run(order=2)
def test__DAG_is_cyclic():
    A, B = get_two_tasks()
    dag = DAG()
    dag.add_dedge(A, B)
    assert not dag.is_cyclic(), 'acyclic graph idenfied as cyclic'
    
    dag = get_cyclic_graph()
    assert dag.is_cyclic(), 'cyclic graph idenfied as acyclic'
