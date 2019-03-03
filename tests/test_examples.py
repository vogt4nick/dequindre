
import pytest

from dequindre import Task, DAG, Dequindre
from dequindre.commons import common_task


def test__readme_example():

    from dequindre import Task, DAG, Dequindre

    ## define tasks and environments
    pour_water = Task('./tea-tasks/pour_water.py')
    boil_water = Task('./tea-tasks/boil_water.py')
    prep_infuser = Task('./tea-tasks/prep_infuser.py')
    steep_tea = Task('./tea-tasks/steep_tea.py')

    ## define runtime dependencies
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


def test__common_task_example():
    from dequindre import DAG, Dequindre
    from dequindre.commons import common_task

    with common_task('./tea-tasks/{}', 'python') as TeaTask:
        boil_water = TeaTask('boil_water.py')
        pour_water = TeaTask('pour_water.py')
        prep_infuser = TeaTask('prep_infuser.py')
        steep_tea = TeaTask('steep_tea.py')

    make_tea = DAG(dependencies={
        boil_water: {pour_water},
        steep_tea: {boil_water, prep_infuser}
    })

    ## run tasks
    dq = Dequindre(make_tea)
    
    dq.run_tasks()


if __name__ == '__main__':
    test__readme_example()
    test__common_task_example()