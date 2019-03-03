
import pytest

from dequindre import common_task, DAG, Dequindre


def test__common_task_exceptions():
    with pytest.raises(AssertionError):
        common_task('/path/to/env')

    with pytest.raises(AssertionError):
        common_task('')

    with pytest.raises(AssertionError):
        common_task('/path/to/env/{}', '')

    with pytest.raises(AssertionError):
        common_task('/path/to/env/{}', None)


def test__common_task():
    CommonTask = common_task('./tea-tasks/{}', 'python')

    boil_water = CommonTask('boil_water.py')
    pour_water = CommonTask('pour_water.py')
    prep_infuser = CommonTask('prep_infuser.py')
    steep_tea = CommonTask('steep_tea.py')

    make_tea = DAG(dependencies={
        boil_water: {pour_water},
        steep_tea: {boil_water, prep_infuser}
    })

    ## run tasks
    dq = Dequindre(make_tea)
    dq.get_schedules()
    # defaultdict(<class 'set'>, {
    #     1: {Task(prep_infuser.py), Task(pour_water.py)},  
    #     2: {Task(boil_water.py)},  
    #     3: {Task(steep_tea.py)}})

    ## dq.run_tasks() can run the files if they exist. 
    
    dq.run_tasks()