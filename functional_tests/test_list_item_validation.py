from unittest import skip
from .base import FunctionalTest, need_wait_decorator
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):
    @need_wait_decorator
    def have_error_text(self, text, css_selector='.has-error'):
        self.assertEqual(
            self.browser.find_element_by_css_selector(css_selector).text,
            text
        )

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        self.have_error_text("You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        # She receives a similar warning on the list page
        self.have_error_text("You can't have an empty list item")
        # And she can correct it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
