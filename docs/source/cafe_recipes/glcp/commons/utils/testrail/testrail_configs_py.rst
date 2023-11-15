testrail_configs.py
===================

``testrail_configs.py`` defines the ``testrail_configs`` data structure used to populate test results in TestRail. This file needs to be placed in ``automation/configs/`` folder of your CAFE repo.

.. code-block::

    from datetime import datetime

    now = datetime.utcnow()
    date_tag = now.strftime("%B-%d-%Y")
    time_tag = now.strftime("%B-%d-%Y-%H:%M:%S")

    suite = "Simple_Test_Plan_for_CAFE_POC"
    cluster = "MyCluster"
    test_type = "Regression"

    # For more details, refer to
    # https://hpe.atlassian.net/wiki/spaces/GST/pages/2083754495/TestRail+User+Guide
    testrail_configs = {
        "project": "SystemQA_POC",
        "milestone": "My_Regression",
        "child_milestone": f"{test_type}",
        "test_suite": f"{suite}",
        "test_plan": f"{suite}-plan-{cluster}-{date_tag}",
        "test_run": f"{suite}-run-{cluster}-{time_tag}-UTC",
        "tc_ids": [1365368, 1365369, 1365370, 1365371],
        "config_ids": [],

    
