Recipe: Get Current GLCP Milestone
==================================

The method ``get_current_milestone`` can be used to figure out the current GLCP milestone.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail.PyTestRail()`

Usage:
    * pytest ``-s`` option sends output to stdout.

::

    % pytest -s get_current_glcp_milestone.py

Sample Output:

::

    Current milestone: Helsinki-Sprint4 (1216)

Code:

.. code-block::

    import os
    import re
    from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail import PyTestRail

    username = os.environ["TR_USERNAME"]
    password = os.environ["TR_PASSWORD"]

    def test_get_current_glcp_milestone():
        tr = PyTestRail(username=username, password=password)
        result = tr.get_current_milestone()  # default project is 'GLCP'
        assert re.match(r".+-Sprint\d", result["name"])
        print(f"\n\nCurrent milestone: {result['name']} ({result['id']})")
