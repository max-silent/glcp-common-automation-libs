Recipe: Populate Automated Test Results
=======================================

This recipe demonstrates how to populate test results into TestRail when a Pytest script executes.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_plugin.PyTestRailPlugin()`
    * :doc:`conftest.py <conftest_py>`
    * :doc:`testrail_configs.py <testrail_configs_py>`
    * Confluence test plan (e.g., `Simple Test Plan for CAFE POC <https://hpe.atlassian.net/wiki/spaces/GST/pages/2126874467/Simple+Test+Plan+for+CAFE+POC>`_)
        * The assumption is that you have imported your test cases into a TestRail suite. Refer to `TestRail User Guide <https://hpe.atlassian.net/wiki/spaces/GST/pages/2083754495/TestRail+User+Guide>`_ for more details.

Usage:
    * Create ``conftest.py`` using the above example.
    * Create ``testrail_configs.py`` using the above example.
    * Configure ``testrail_configs.py``
        * Map TestRail Test Case IDs to Pytest functions/methods using the decorator ``@pytest.mark.testrail()``.

          ::

              @pytest.mark.testrail(id=1365368)
              def test_get_list_all_pets(self):
                  assert True

    * Execute Pytest script. You need to specify the TestRail credentials. See sample output below.

      ::

          % TR_USERNAME=XXX TR_PASSWORD=XXX pytest test_simple_test_plan_for_cafe_poc.py.py

          ============================================================ test session starts =============================================================
          ...

          populate_automated_test_results.py::TestSimpleTestPlanForCafePoc::test_get_list_all_pets PASSED                                        [ 25%]
          populate_automated_test_results.py::TestSimpleTestPlanForCafePoc::test_post_add_a_pet PASSED                                           [ 50%]
          populate_automated_test_results.py::TestSimpleTestPlanForCafePoc::test_adding_a_new_region_for_sample_application FAILED               [ 75%]
          populate_automated_test_results.py::TestSimpleTestPlanForCafePoc::test_removing_a_region_for_the_sample_application FAILED             [100%]

          Uploading results to TestRail...
            Project: SystemQA_POC, id: 6
            Milestone: TestRail-CAFE-Milestone-milestone, id: 1286
            Sub Milestone: Pytest_Run1, id: 1287
            Suite: Simple_Test_Plan_for_CAFE_POC, id: 542
            Suite Section: Suite_1, id: 23156
            Test Plan: Simple-Test-Plan-for-CAFE-POC-plan-July-19-2023, id: 17596
            Test Run: Simple-Test-Plan-for-CAFE-POC-run-July-19-2023-14:32:39-UTC, id: 17600

          ...

          test_simple_test_plan_for_cafe_poc.py.py:19: AssertionError
          ========================================================== short test summary info ===========================================================
          FAILED test_simple_test_plan_for_cafe_poc.py.py::TestSimpleTestPlanForCafePoc::test_adding_a_new_region_for_sample_application - assert False
          FAILED test_simple_test_plan_for_cafe_poc.py.py::TestSimpleTestPlanForCafePoc::test_removing_a_region_for_the_sample_application - assert False
          ======================================================== 2 failed, 2 passed in 7.37s =========================================================

    * Verify that test results have been updated in TestRail. For project milestone **TestRail-CAFE-Milestone-milestone** used in the above ``testrail_configs``, you can find the test results at https://testrail.glcp.hpedev.net/index.php?/milestones/view/1286 .


Code:

.. code-block::

    import pytest


    class TestSimpleTestPlanForCafePoc:
        @pytest.mark.testrail(id=1365368)
        def test_get_list_all_pets(self):
            assert True
    
        @pytest.mark.testrail(id=1365369)
        def test_post_add_a_pet(self):
            assert True
    
        @pytest.mark.testrail(id=1365370)
        def test_adding_a_new_region_for_sample_application(self):
            assert False
    
        @pytest.mark.testrail(id=1365371)
        def test_removing_a_region_for_the_sample_application(self):
            assert False
    
