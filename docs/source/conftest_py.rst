conftest.py
===========

``conftest.py`` defines the Pytest fixtures and browser initializations.

.. code-block::

    import pytest
    import os
    
    def browser_type(playwright, browser_name: str):
        """
        Playwright browser type to be used by the test scripts
        """
        if browser_name == "chromium":
            browser = playwright.chromium
            if os.getenv("POD_NAMESPACE") is None:
                return browser.launch(headless=False, slow_mo=100)
            else:
                return browser.launch(headless=True, slow_mo=100)
        if browser_name == "firefox":
            browser = playwright.firefox
            if os.getenv("POD_NAMESPACE") is None:
                return browser.launch(headless=False, slow_mo=100)
            else:
                return browser.launch(headless=True, slow_mo=100)
        if browser_name == "webkit":
            browser = playwright.webkit
            if os.getenv("POD_NAMESPACE") is None:
                return browser.launch(headless=False, slow_mo=100)
            else:
                return browser.launch(headless=True, slow_mo=100)
    
    @pytest.fixture(scope="session")
    def browser_instance(playwright):
        """
        Tests create browser instance with this function to create chromium browser
        """
        browser = browser_type(playwright, "chromium")
        yield browser
    
    
    @pytest.fixture(scope="session")
    def page(browser_instance):
        context = browser_instance.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser_instance.close()

