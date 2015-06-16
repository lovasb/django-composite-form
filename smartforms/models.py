from django.db import transaction

from .forms import CompositeForm


class CompositeModelForm(CompositeForm):
    def __init__(self, *args, **kwargs):
        super(CompositeModelForm, self).__init__(*args, **kwargs)
        if not all(hasattr(obj, 'save') for obj in self._subforms):
            raise ValueError('all form instance must have save method (model form)')

    def save(self, commit=True):
        with transaction.atomic():
            for form in self._subforms:
                form.save(commit=commit)