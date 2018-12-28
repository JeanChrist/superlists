from django.test import TestCase
from ..models import Item, List


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
