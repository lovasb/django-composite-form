from django import forms
from django.test import TestCase

from .forms import Form1, Form1Dedup, Form2
from composite_form.forms import CompositeForm


class ClassInitTest(TestCase):
    def test_empty_init(self):
        """
        Test empty initialization: all subforms are reprezented in the list, and none of them is bounded.
        """
        form_classes = [Form1, Form2]
        form = CompositeForm(form_classes=form_classes)
        for i in range(0, len(form._subforms)):
            act = form._subforms[i]
            self.assertIsInstance(act, form_classes[i])
            self.assertEquals(act.is_bound, False)
        self.assertEquals(form.is_bound, False)

    def test_post_init(self):
        """
        Passing POST data to parent form -> the form is bounded (and all subforms to).
        """
        post = {'data': 'example'}
        form_classes = [Form1, Form2]
        form = CompositeForm(data=post, form_classes=form_classes)
        self.assertEquals(form.is_bound, True)

    def test_fields_represented(self):
        """
        Subform fields are represented in CompositeForm
        """
        form_classes = [Form1, Form2]
        form = CompositeForm(form_classes=form_classes)
        fields = form.fields

        fields2 = Form1().fields
        fields2.update(Form2().fields)

        self.assertEquals(fields.keys(), fields2.keys())

    def test_deduplicate_fields(self):
        """
        Multiple form fields are deduplicated, and last defined is used.
        """
        class DedupForm(forms.Form):
            field1 = forms.CharField()
            field1 = forms.IntegerField()

        fields1 = DedupForm().fields

        form = CompositeForm(form_classes=[Form1, Form1Dedup])
        fields2 = form.fields

        self.assertEquals(fields1.keys(), fields2.keys())
        self.assertEquals(len(fields2.keys()), 1)


class InstanceInitTest(TestCase):
    def test_both_error(self):
        form_instances = [Form1(), Form2()]
        form_classes = [Form1, Form2]

        self.assertRaises(AttributeError, lambda: CompositeForm(form_instances=form_instances, form_classes=form_classes))

    def test_init_with_instances(self):
        post_data = {'field1': 'example', 'field2': 1}
        form1 = Form1(data=post_data)
        form2 = Form2(data=post_data)

        form = CompositeForm(form_instances=[form1, form2])
        self.assertEquals(len(form._subforms), 2)
        self.assertEquals(form.is_valid(), True)