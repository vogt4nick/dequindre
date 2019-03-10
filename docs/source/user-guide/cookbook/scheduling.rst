Scheduling
----------

Dequindre's schedule submodule is forked from `v0.6 of the schedule module`_ 
created by Daniel Bader and other supporting authors.

.. _v0.6 of the schedule module: https://github.com/dbader/schedule/tree/0.6.0


Schedule a Workflow
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def my_workflow():
        ...

    if __name__ == '__main__':
        schedule.every(10).minutes.do(my_workflow)
        while True:
            schedule.run_pending()
