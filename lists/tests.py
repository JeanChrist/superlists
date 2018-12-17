from django.test import TestCase
from .models import Item
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

    def test_can_post_and_save_a_item(self):
        data = {'item_text': 'A new test item'}
        response = self.client.post(self.url, data=data)
        self.assertIn(data['item_text'], response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def setUp(self):
        self.model = Item

    def test_saving_and_retrieving_items(self):
        # self.model.objects.create
        first_item = self.model()
        first_text = 'The first (ever) list item'
        first_item.text = first_text
        first_item.save()

        second_item = self.model()
        second_text = 'Item the second'
        second_item.text = second_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_text)
        self.assertEqual(second_saved_item.text, second_text)
