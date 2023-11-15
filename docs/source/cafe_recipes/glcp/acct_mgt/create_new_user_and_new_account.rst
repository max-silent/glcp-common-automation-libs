Recipe: Create a New GLCP User and a new Account
================================================

Create a new GLCP User and a new Account.

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.acct_mgmt.helpers.ui_am_create_new_user_new_acct_setup`
    * :doc:`conftest.py <../../../conftest_py>` - Use the ``page`` fixture

.. code-block::

    import os
    from hpe_glcp_automation_lib.libs.acct_mgmt.helpers.ui_am_create_new_user_new_acct_setup import HlpCreateUserCreateAcct
    from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
    import logging
    
    cluster_url = os.environ["CLUSTER_URL"]
    gmail_username = os.environ["GMAIL_USER_NAME"]
    gmail_password = os.environ["GMAIL_USER_PASSWORD"]
    
    log = logging.getLogger(__name__)
    
    
    def test_create_new_user_and_new_account(page):
        acct_name = RandomGenUtils.random_string_of_chars(7)
        glcpuser_email = (
            gmail_username.split("@")[0]
            + "+"
            + str(acct_name)
            + "@"
            + gmail_username.split("@")[1]
        )
        
        gmail_creds = (gmail_username, gmail_password)  # a tuple
        new_acc = HlpCreateUserCreateAcct(gmail_creds)
        customer_details = new_acc.svc_new_user_signup(
            page, cluster_url, glcpuser_email, acct_name
        )
        if customer_details:
            log.info("customer details: {}".format(customer_details))
