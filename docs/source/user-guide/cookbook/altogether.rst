Bringing It All Together
========================

.. code-block:: python

    from pprint import pprint

    from dequindre import Task, DAG, Dequindre
    from dequindre.commons import common_task, common_conda_env


    def run_schedule():
        print('Starting run-my-schedule...')

        CONDA_PREFIX = '/opt/conda/envs'
        with common_conda_env(CONDA_PREFIX) as conda_env:
            python27 = conda_env('python27')
            python36 = conda_env('python36')

        TASK_PATTERN = '/opt/my-tasks/{}/main.py'
        with common_task(TASK_PATTERN, python27) as T:
            leave_home    = T('leave_home')
            get_fuel      = T('get_fuel')
            get_groceries = T('get_groceries')

        with common_task(TASK_PATTERN, python36) as T:
            pay_rent      = T('pay_rent')
            return_home   = T('return_home')
            make_dinner   = T('make_dinner')
            go_to_bed     = T('go_to_bed')

        dag = DAG(tasks={
            leave_home, get_fuel, get_groceries, 
            pay_rent, return_home, make_dinner, go_to_bed
        })
        dag.add_dependencies({
            get_fuel: leave_home,
            get_groceries: leave_home,
            pay_rent: leave_home,
            return_home: {get_fuel, get_groceries, pay_rent},
            make_dinner: {return_home, get_groceries},
            go_to_bed: make_dinner
        })

        dq = Dequindre(dag)
        schedules = dq.get_schedules()
        pprint(schedules)
        # {1: {Task(/opt/my-tasks/leave_home/main.py)},
        #  2: {Task(/opt/my-tasks/get_fuel/main.py),
        #      Task(/opt/my-tasks/pay_rent/main.py),
        #      Task(/opt/my-tasks/get_groceries/main.py)},
        #  3: {Task(/opt/my-tasks/return_home/main.py)},
        #  4: {Task(/opt/my-tasks/make_dinner/main.py)},
        #  5: {Task(/opt/my-tasks/go_to_bed/main.py)}}

        dq.run_tasks()


    if __name__ == '__main__':
        run_schedule()

