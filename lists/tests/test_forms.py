from django.test import TestCase
from ..models import List, Item
from ..forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm


class ItemFormTest(TestCase):
    def setUp(self):
        self.form_class = ItemForm

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = self.form_class()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = self.form_class(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        form = self.form_class(data={'text': 'do me'})
        list_ = List.objects.create()
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)

    def test_form_validation_for_duplicate_items(self):
        list_obj = List.objects.create()
        data = {'text': 'do me'}
        ExistingListItemForm(list_obj, data=data).save(list_obj)
        form = ExistingListItemForm(list_obj, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])
