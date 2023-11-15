Recipe: Login to GLCP through API and return devices information
================================================================

Login to GLCP through API call and returns JSON of devices list in that account with their information 

Dependencies:
    * :py:meth:`hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway`

.. code-block::

    import os
    import logging
    from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

    log = logging.getLogger(__name__)
    
    cluster_url = os.environ["CLUSTER_URL"]  # e.g., "https://polaris.ccs.arubathena.com"
    username = os.environ["USER_NAME"]
    password = os.environ["USER_PASSWORD"]
    pcid = os.environ["PCID"]  # Platform Customer ID
    

    def test_api_login_list_devices():
        APISession = UIDoorway(cluster_url, username, password, pcid)
        temp = APISession.list_devices()
        log.info(temp)
