from django.test import TestCase

from ..forms import ItemForm, EMPTY_ITEM_ERROR


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
