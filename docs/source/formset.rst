
FormSet
=======

FormSet main goal is the same as `django formsets <https://docs.djangoproject.com/en/dev/topics/forms/formsets/>`_ ,
but the implementation and the API differs a bit. FormSet object is a more ``django.forms.Form`` like object.
Basic usage:

.. highlight:: python
>>> from smartforms import FormSet
>>> class Form1(forms.Form):
        field1 = forms.CharField()
        field2 = forms.IntegerField()
>>> form = FormSet(form_class=Form1, repeat=2, label_suffix='suff')
>>> form.is_valid()
>>> False
