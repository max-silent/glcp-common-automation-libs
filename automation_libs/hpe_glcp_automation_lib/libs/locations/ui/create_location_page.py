import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.navigation.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.locations.ui.locators import CreateLocationPageSelectors

log = logging.getLogger(__name__)


class CreateLocationPage(HeaderedPage):
    """
    Create Location page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Create Location page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Create Location page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/locations/create-location"

    def click_create_location(self):
        """
        Clicks the Create Location button
        """
        log.info("Playwright clicking create location button")
        self.page.locator(CreateLocationPageSelectors.CREATE_LOCATION_BTN).click()
        # NOTE cannot return Location page object as it would result in a circular import conflict

    def click_next_button(self):
        """
        Clicks the next page button
        return: self reference
        """
        log.info("Playwright: clicking next page button")
        self.page.locator(CreateLocationPageSelectors.NEXT_BUTTON).click()
        return self

    def fill_location_name(self, name):
        """
        Fills out Location Name field
        :params name: Name of location to be created
        return: self reference
        """
        log.info(f"Playwright: entering {name} into location name field")
        self.page.locator(CreateLocationPageSelectors.LOCATION_NAME_INPUT).fill(name)
        return self

    def fill_location_description(self, description):
        """
        Fills out Location description field
        :params description: Name of location to be created
        return: self reference
        """
        log.info(f"Playwright: entering {description} into location description field")
        self.page.locator(CreateLocationPageSelectors.LOCATION_DESC_INPUT).fill(
            description
        )
        return self

    def add_location_address(
        self, country, street_address, city, state, postcode, street_address_2=None
    ):
        """
        Adds an address in the location creation page
        :params country: option to be entered in the country field
        :params street_address: text to be entered in the street_address field
        :params city: text to be entered in the city field
        :params state: text to be entered in the state field
        :params postcode: text to be entered in the postcode field
        :params street_address_2: optional text to be entered in the street_address_2 field
        return: self reference
        """
        log.info("Playwright: filling out address form")
        self.page.locator(CreateLocationPageSelectors.OPEN_ADD_ADDRESS_BTN).click()
        self.pw_utils.select_drop_down_element(
            CreateLocationPageSelectors.COUNTRY_DROPDOWN, country, element_role="option"
        )
        self.page.locator(CreateLocationPageSelectors.STREET_ADDRESS_INPUT).fill(
            street_address
        )
        self.page.locator(CreateLocationPageSelectors.CITY_ADDRESS_INPUT).fill(city)
        self.page.locator(CreateLocationPageSelectors.STATE_ADDRESS_INPUT).fill(state)
        self.page.locator(CreateLocationPageSelectors.POSTCODE_INPUT).fill(postcode)
        if street_address_2 is not None:
            self.page.locator(CreateLocationPageSelectors.STREET_ADDRESS_2_INPUT).fill(
                street_address_2
            )
        self.page.locator(CreateLocationPageSelectors.APPLY_ADD_ADDRESS_BTN).click()
        return self

    def assign_contact(self, type, username, phone=None):
        """
        Assigns a contact to a location in the create location page
        :params type: Type to be assigned to contact
        :params username: Contact Username
        :params phone: Contact Phone Number
        return: self reference
        """
        log.info("Playwright assigning contact to location")
        self.pw_utils.select_drop_down_element(
            CreateLocationPageSelectors.CONTACT_TYPE_DROPDOWN, type, element_role="option"
        )
        self.pw_utils.select_drop_down_element(
            CreateLocationPageSelectors.CONTACT_USER_DROPDOWN,
            username,
            element_role="option",
        )
        if phone is not None:
            self.page.locator(CreateLocationPageSelectors.CONTACT_PHONE_INPUT).fill(phone)
        self.page.locator(CreateLocationPageSelectors.ASSIGN_CONTACT_BTN).click()
        return self

    def cancel_setup(self):
        """
        Clicks the cancel setup button
        return: self reference
        """
        log.info("Playwright: clicking cancel setup button")
        self.page.locator(CreateLocationPageSelectors.CANCEL_SETUP_BTN).click()
        self.page.locator(CreateLocationPageSelectors.CONFIRM_CANCEL_BTN).click()
        return self

    def should_have_location_title(self, text):
        """
        Verify Location Page title
        param: text in title
        return: self reference
        """
        log.info(
            f"Playwright: check that wizard heading with '{text}' text is displayed."
        )
        self.page.wait_for_load_state()
        expect(
            self.page.locator(CreateLocationPageSelectors.SERVICE_PAGE_HEADING)
        ).to_have_text(text)
        return self
