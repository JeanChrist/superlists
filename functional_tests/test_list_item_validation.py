from unittest import skip
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))
        # self.have_error_text()

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)
        # She receives a similar warning on the list page
        # self.have_error_text()
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):

        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        text = 'Buy wellies'
        self.get_item_input_box().send_keys(text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table(f'1: {text}')
        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys(text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            DUPLICATE_ITEM_ERROR
        ))
