from selenium import webdriver
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(r'D:\WorkSpace\chromedriver.exe')

    def tearDown(self):
        self.browser.quit()

    def test_1(self):
        self.browser.get('http://localhost:6789')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')


if __name__ == '__main__':

    unittest.main(warnings='ignore')
