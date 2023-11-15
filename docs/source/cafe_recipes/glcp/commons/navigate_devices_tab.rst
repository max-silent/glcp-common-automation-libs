Recipe: Navigate to Devices Tab
===============================

Login to an existing GLCP user account and navigate to the Devices tab.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.authn.ui.login_page.Login`
    * :py:meth:`hpe_glcp_automation_lib.libs.commons.ui.elem_nav_bar`
    * :doc:`conftest.py <../../../conftest_py>` - Use the ``page`` fixture

.. code-block::

    import os
    from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
    from hpe_glcp_automation_lib.libs.commons.ui.elem_nav_bar import NavigationBar
    
    cluster_url = os.environ["CLUSTER_URL"]         # e.g., "https://polaris.ccs.arubathena.com"
    username = os.environ["USER_NAME"]
    password = os.environ["USER_PASSWORD"]
    acct_name = os.environ["GLCP_ACCOUNT_NAME"]  # This should be None if there is only one workspace in the GLCP account
    
    
    def test_navigate_devices_tab(page):
        ui_login = Login(page, cluster_url).open()
        if acct_name:
            ui_login.login_acct(username, password, acct_name).go_to_account_by_name(
                acct_name
            ).wait_for_loaded_state()
        else:
            ui_login.login_acct(username, password).wait_for_loaded_state()
        NavigationBar(page).navigate_to_devices()
    
