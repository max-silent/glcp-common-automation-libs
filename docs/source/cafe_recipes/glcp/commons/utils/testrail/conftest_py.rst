conftest.py
===========

``conftest.py`` defines the Pytest fixtures and browser initializations.

.. code-block::

    from automation.configs.testrail_configs import testrail_configs
    from hpe_glcp_automation_lib.libs.commons.utils.testrail.testrail_plugin import (
        PyTestRailPlugin,
    )

    def pytest_configure(config):
        config.pluginmanager.register(PyTestRailPlugin(testrail_configs))
    
