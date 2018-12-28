from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from django.test import LiveServerTestCase
from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys

MAX_WAIT = 10


def need_wait_decorator(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return wrap


class FunctionalTest(StaticLiveServerTestCase):
    @property
    def new_browser(self):
        return webdriver.Chrome(r'D:\WorkSpace\chromedriver.exe')

    def setUp(self):
        self.browser = self.new_browser
        staging_server = sys.argv[-1]
        # staging_server = os.environ.get('STAGING_SERVER')
        if '.com' in staging_server:
            self.live_server_url = staging_server

    def tearDown(self):
        self.browser.quit()

    @need_wait_decorator
    def check_for_row_in_list_table(self, row_text):

        table = self.browser.find_element_by_id('id_list_table')

        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
