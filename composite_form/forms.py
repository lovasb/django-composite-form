from collections import OrderedDict
from django.forms.utils import ErrorDict


class CompositeForm(object):
    def __init__(self, data=None, files=None, form_classes=[]):
        self.form_classes = form_classes
        self._subforms = []
        self._field_name_mapper = {}

        for i in range(0, len(self.form_classes)):
            prefix = 'form{0}'.format(i)
            form = self.form_classes[i](data, files, prefix=prefix)
            for name in form.fields.keys():
                self._field_name_mapper[name] = i
            self._subforms.append(form)

    def __iter__(self):
        for name in self._field_name_mapper.keys():
            yield self._subforms[self._field_name_mapper[name]][name]

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            name not in self._field_name_mapper.keys()
        except KeyError:
            raise KeyError(
                "Key %r not found in '%s'" % (name, self.__class__.__name__))

        return self._subforms[self._field_name_mapper[name]][name]

    def is_valid(self):
        return all(form.is_bound and not form.errors for form in self._subforms)

    @property
    def is_bound(self):
        return all(form.is_bound for form in self._subforms)

    @property
    def fields(self):
        retval = OrderedDict()
        for form in self._subforms:
            retval.update(form.fields)
        return retval

    @property
    def errors(self):
        _errors = ErrorDict()
        for form in self._subforms:
            _errors.update(form.errors)
        return _errors