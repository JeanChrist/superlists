from django.test import TestCase
from .models import Item, List
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
        list_ = List.objects.create()
        Item.objects.create(text=text1, list=list_)
        Item.objects.create(text=text2, list=list_)
        response = self.client.get(self.url)
        self.assertContains(response, text1)
        self.assertContains(response, text2)


class NewListTest(TestCase):
    def setUp(self):
        self.url = '/lists/create'
        self.success_url = '/lists/the-only-list-in-the-world/'

    def test_can_save_a_POST_request(self):
        data = {'item_text': 'A new list item'}
        self.client.post(self.url, data=data)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, data['item_text'])

    def test_redirects_after_POST(self):
        response = self.client.post(self.url, data={'item_text': 'A new list item'})
        self.assertRedirects(response, self.success_url)


class ListAndItemModelsTest(TestCase):

    def setUp(self):
        self.item_model = Item
        self.list_model = List

    def test_saving_and_retrieving_items(self):
        list_ = self.list_model()
        list_.save()

        # self.model.objects.create
        first_item = self.item_model()
        first_text = 'The first (ever) list item'
        first_item.text = first_text
        first_item.list = list_
        first_item.save()

        second_item = self.item_model()
        second_text = 'Item the second'
        second_item.text = second_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_text)
        self.assertEqual(second_saved_item.list, list_)
