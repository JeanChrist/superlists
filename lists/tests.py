from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string


# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        self.url = '/'

    def test_uses_home_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'home.html')
