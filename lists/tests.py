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
        self.template_name = 'home.html'

    def test_uses_home_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        data = {'item_text': 'A new test item'}
        self.client.post(self.url, data=data)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, data['item_text'])

    def test_redirects_after_POST(self):
        response = self.client.post(self.url, data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    #
    # def test_displays_all_list_items(self):
    #     text1, text2 = 'itemey 1', 'itemey 2'
    #     Item.objects.create(text=text1)
    #     Item.objects.create(text=text2)
    #     response = self.client.get(self.url)
    #     self.assertIn(text1, response.content.decode())
    #     self.assertIn(text2, response.content.decode())


class ListViewTest(TestCase):
    def setUp(self):
        self.url = '/lists/the-only-list-in-the-world/'
        self.template_name = 'list.html'

    def test_used_list_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_displays_all_items(self):
        text1, text2 = 'itemey 1', 'itemey 2'
        Item.objects.create(text=text1)
        Item.objects.create(text=text2)
        response = self.client.get(self.url)
        self.assertContains(response, text1)
        self.assertContains(response, text2)


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
