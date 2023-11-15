Recipe: Get Test Cases
======================

Get the list of test cases (IDs, sections, titles) for a given suite/project.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail.PyTestRail()`

Usage:
    * pytest ``-s`` option sends output to stdout.

::

    % pytest -s get_test_cases.py

Sample Output:

::

    Case IDs:
    ['1365368: Global / GET - List all pets',
     '1365369: Global / POST - Add a pet',
     '1365370: Regional/Region1 / Adding a new region for sample application',
     '1365371: Regional/Region1 / Removing a region for the sample application']

Code:

.. code-block::

    import os
    import pprint
    from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail import PyTestRail
    
    username = os.environ["TR_USERNAME"]
    password = os.environ["TR_PASSWORD"]
    project_name = os.getenv("TR_PROJECT_NAME") or "SystemQA_POC"
    suite_name = os.getenv("TR_SUITE_NAME") or "Simple Test Plan for CAFE POC"
    
    def test_get_test_cases():
        tr = PyTestRail(username=username, password=password)
        project_id = tr.get_project_id(project_name)
        suite_id = tr.get_suite_id(project_id, suite_name)
        result = tr.get_cases(project_id, suite_id)
    
        all_test_cases = [
            f"{x['id']}: {tr.get_section(x['section_id'])['name']} / {x['title']}"
            for x in result
        ]
        print(f"Case IDs:\n{pprint.pformat(all_test_cases, indent=1, width=80)}")

