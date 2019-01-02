from django.test import TestCase
from ..models import Item, List
from ..forms import ItemForm
from django.utils.html import escape


# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        self.url = '/'
        self.template_name = 'home.html'

    def test_uses_home_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, self.template_name)

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post(self.url, data={'item_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post(self.url, data={'item_text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(self.url, data={'item_text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
