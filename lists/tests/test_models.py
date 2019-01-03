from django.test import TestCase
from ..models import Item, List
from django.core.exceptions import ValidationError


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

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()

        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()

        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()

        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()

        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean()  # should not raise
