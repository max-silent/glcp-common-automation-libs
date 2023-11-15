Recipe: Login and Go to Account
===============================

Login to an existing GLCP user account and then open up the company account.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.authn.ui.login_page.Login`
    * :doc:`conftest.py <../../../conftest_py>` - Use the ``page`` fixture

.. code-block::

    import os
    from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
    
    cluster_url = os.environ["CLUSTER_URL"]      # e.g., "https://polaris.ccs.arubathena.com"
    username = os.environ["USER_NAME"]
    password = os.environ["USER_PASSWORD"]
    acct_name = os.environ["GLCP_ACCOUNT_NAME"]  # This should be None if there is only one workspace in the GLCP account
    
    
    def test_login_go_to_account(page):
        ui_login = Login(page, cluster_url).open()
        if acct_name:
            ui_login.login_acct(username, password, acct_name).go_to_account_by_name(
                acct_name
            ).wait_for_loaded_state()
        else:
            ui_login.login_acct(username, password).wait_for_loaded_state()
    
