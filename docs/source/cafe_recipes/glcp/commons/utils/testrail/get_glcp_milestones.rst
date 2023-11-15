Recipe: Get GLCP Milestones
===========================

Get the milestones for GLCP project.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail.PyTestRail()`

Usage:
    * pytest ``-s`` option sends output to stdout.

::

    % pytest -s get_glcp_milestones.py

Sample Output:

::

    Project: GLCP

    Activate-SM-Test-Automation (1020)                 start_on: None                 started_on: 2023-04-27 00:00:00  due_on: 2023-05-16 00:00:00  completed: False
    GLCP-Dark-And-Dim-Sites (1152)                     start_on: None                 started_on: 2023-05-22 21:53:16  due_on: None                 completed: False
    Helsinki-Sprint4 (1216)                            start_on: None                 started_on: 2023-08-01 23:30:53  due_on: 2023-08-15 18:30:00  completed: False
    Helsinki-Sprint5 (1226)                            start_on: 2023-08-16 18:30:00  started_on: None                 due_on: 2023-08-29 18:30:00  completed: False
    Helsinki-Sprint6 (1236)                            start_on: 2023-08-30 18:30:00  started_on: None                 due_on: 2023-09-12 18:30:00  completed: False
    Helsinki-Sprint7 (1246)                            start_on: 2023-09-13 18:30:00  started_on: None                 due_on: 2023-09-26 18:30:00  completed: False
    Helsinki-Sprint8 (1256)                            start_on: 2023-09-27 18:30:00  started_on: None                 due_on: 2023-10-10 18:30:00  completed: False

Code:

.. code-block::

    import os
    from datetime import datetime
    from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail import PyTestRail

    username = os.environ["TR_USERNAME"]
    password = os.environ["TR_PASSWORD"]
    project_name = "GLCP"
    show_active = True  # Only show active milestones (i.e., not completed)

    def test_get_glcp_milestones():
        tr = PyTestRail(username=username, password=password)
        project_id = tr.get_project_id(project_name)
        result = tr.get_milestones(project_id)

        print(f"\n\nProject: {project_name}\n")
        for x in result:
            milestone = f"{x['name']} ({x['id']})"
            start_on = x["start_on"]
            started_on = x["started_on"]
            due_on = x["due_on"]
            is_completed = x["is_completed"]

            if start_on:
                start_on = datetime.utcfromtimestamp(start_on)
            else:
                start_on = "None"

            if started_on:
                started_on = datetime.utcfromtimestamp(started_on)
            else:
                started_on = "None"

            if due_on:
                due_on = datetime.utcfromtimestamp(due_on)
            else:
                due_on = "None"

            if show_active and is_completed:
                pass  # ignore completed milestones
            else:
                print(
                    f"{milestone:50}"
                    f" start_on: {str(start_on):20}"
                    f" started_on: {str(started_on):20}"
                    f" due_on: {str(due_on):20}"
                    f" completed: {is_completed}"
                )
