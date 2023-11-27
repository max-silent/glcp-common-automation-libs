"""
Headered page base class for page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.locators import HeaderedPageSelectors
from hpe_glcp_automation_lib.libs.commons.ui.navigation.elem_nav_bar import NavigationBar

log = logging.getLogger(__name__)


class HeaderedPage(BasePage):
    """
    HeaderedPage page object model.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize HeaderedPage page object.
        :param page: page.
        :param cluster: cluster url.
        """
        super().__init__(page, cluster)
        self.nav_bar = NavigationBar(page)

    def close_contextual_help(self):
        """Clicking on close button of the contextual help.
        :return: instance of current page object.
        """
        log.info(f"Playwright clicking on close button contextual help menu option")
        self.page.wait_for_load_state()
        self.page.locator(HeaderedPageSelectors.CONTEXTUAL_HELP_CLOSE_BTN).click()
        return self

    def click_on_contextual_help_option(self, contextual_help):
        """Clicking on any of the contextual help options.
        :param contextual_help: text of contextual help option.
        :return: instance of current page object.
        """
        log.info(f"Playwright clicking on contextual help menu option {contextual_help}")
        self.page.wait_for_load_state()
        self.page.locator(
            HeaderedPageSelectors.CONTEXTUAL_HELP_ITEM_TEMPLATE.format(contextual_help)
        ).click()
        return self

    def click_on_back_to_contextual_help_menu(self):
        """Clicks on previous button to go back to the contextual help
        menu when you are on a sub topic in the contextual help.
        :return: instance of current page object.
        """
        log.info("Playwright clicking on contextual help back to menu")
        self.page.locator(HeaderedPageSelectors.BACK_TO_LIST).click()
        return self

    def should_have_context_help_option(self, contextual_help):
        """Verifying the existence on any of the contextual help options.
        :param contextual_help: text of contextual help option.
        :return: instance of current page object.
        """
        log.info(
            f"Playwright: verifying visibility of contextual help menu option '{contextual_help}'."
        )
        self.page.wait_for_load_state()
        expect(
            self.page.locator(
                HeaderedPageSelectors.CONTEXTUAL_HELP_ITEM_TEMPLATE.format(
                    contextual_help
                )
            )
        ).to_be_visible()
        return self

    def should_have_context_help_url(self, url):
        """Checking the hyperlink matches.
        :param url: expected url of contextual help hyperlink.
        :return: instance of current page object.
        """
        log.info(f"Playwright: verifying url of contextual help menu option '{url}'.")
        expect(
            self.page.locator(
                HeaderedPageSelectors.CONTEXTUAL_HELP_URL_TEMPLATE.format(url)
            )
        ).to_be_visible()
        return self

    def should_have_contextual_help_title(self, title_text):
        """Verifying the existence of title on any of the contextual help options.
        :param title_text: title text of contextual help option.
        :return: instance of current page object.
        """
        log.info(
            f"Playwright: verifying visibility of contextual help menu title: '{title_text}'."
        )
        self.page.wait_for_load_state()
        expect(
            self.page.locator(
                HeaderedPageSelectors.CONTEXTUAL_HELP_TITLE_TEMPLATE.format(title_text)
            )
        ).to_be_visible()
        return self

    def should_have_view_all_documentation(self):
        """Checking the view all documentation button.
        :return: instance of current page object.
        """
        expect(
            self.page.locator(HeaderedPageSelectors.VIEW_ALL_DOCUMENTATION)
        ).to_be_visible()
        return self

    def should_have_expected_subtopics(self, expected_subtopics_list):
        """
        Checks that the number of subtopics and the actual subtopics in the contextual help menu match what is expected

        :param expected_subtopics_list: list of expected subtopics
        :return: instance of current page object.
        """

        actual_subtopics_list = self.page.locator(
            HeaderedPageSelectors.LIST_OF_ALL_TOPICS
        ).all_inner_texts()
        assert len(expected_subtopics_list) == len(
            actual_subtopics_list
        ), "Number of expected subtopics and actual subtopics dont match"
        assert sorted(expected_subtopics_list) == sorted(
            actual_subtopics_list
        ), f"Expected subtopics doesn't match actual subtopics"
        return self
