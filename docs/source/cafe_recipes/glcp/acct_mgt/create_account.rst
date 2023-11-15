Recipe: Create a New Account
===============================

Login to an existing GLCP user and then create a new Account.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.authn.ui.login_page.Login`
    * :py:meth:`hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_account_page.CreateAcctPage`
    * :doc:`conftest.py <../../../conftest_py>` - Use the ``page`` fixture

.. code-block::

    import os
    from hpe_glcp_automation_lib.libs.authn.ui.login_page import Login
    from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_account_page import CreateAcctPage
    
    cluster_url = os.environ["CLUSTER_URL"]  # e.g., "https://polaris.ccs.arubathena.com"
    username = os.environ["USER_NAME"]
    password = os.environ["USER_PASSWORD"]
    

    def test_create_account(page):
        ui_login = Login(page, cluster_url).open()
        ui_login.login_acct(username, password)
        create_acct_page = CreateAcctPage(page, cluster_url).open()
        create_acct_page.create_acct().wait_for_loaded_state()
