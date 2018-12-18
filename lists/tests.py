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
        self.list = List.objects.create()

        self.url = self.list.get_absolute_url()
        self.template_name = 'list.html'

    def test_used_list_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_passes_correct_list_to_template(self):
        # other_list = List.objects.create()

        # correct_list = List.objects.create()
        response = self.client.get(self.url)
        self.assertEqual(response.context['list'], self.list)

    def test_displays_only_items_for_that_list(self):
        # correct_list =
        text1, text2 = 'itemey 1', 'itemey 2'
        Item.objects.create(text=text1, list=self.list)
        Item.objects.create(text=text2, list=self.list)
        other_list = List.objects.create()
        other_text1, other_text2 = 'other list item 1', 'other list item 2'
        Item.objects.create(text=other_text1, list=other_list)
        Item.objects.create(text=other_text2, list=other_list)
        response = self.client.get(self.url)
        self.assertContains(response, text1)
        self.assertContains(response, text2)
        self.assertNotContains(response, other_text1)
        self.assertNotContains(response, other_text2)


class NewListTest(TestCase):
    def setUp(self):
        self.item_model = Item
        self.url = '/lists/create'
        self.success_url = '/lists/the-only-list-in-the-world/'

    def test_can_save_a_POST_request(self):
        data = {'item_text': 'A new list item'}
        self.client.post(self.url, data=data)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, data['item_text'])

    def test_redirects_after_POST(self):
        data = {'item_text': 'A new list item'}
        response = self.client.post(self.url, data=data)
        item_obj = self.item_model.objects.get(text=data['item_text'])
        self.assertRedirects(response, item_obj.list.get_absolute_url())


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


class NewItemTest(TestCase):
    def setUp(self):
        # self.model = Item
        self.list = List.objects.create()
        self.url = f'/lists/{self.list.id}/add_item'

    def test_can_save_a_POST_request_to_an_existing_list(self):
        # other_list = self.model.objects.create()
        # correct_list = self.model.objects.create()
        data = {'item_text': 'A new item for an existing list'}
        self.client.post(
            self.url,
            data=data
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, data['item_text'])
        self.assertEqual(new_item.list, self.list)

    def test_redirects_to_list_view(self):

        response = self.client.post(
            self.url,
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, self.list.get_absolute_url())
