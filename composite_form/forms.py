from copy import deepcopy
from collections import OrderedDict
from django.forms.utils import ErrorDict


class CompositeForm(object):
    def __init__(self, data=None, files=None, form_classes=[], form_instances=[]):
        if len(form_instances) and len(form_classes):
            raise AttributeError('form_classes and form_instances could not be setted')

        self.form_classes = form_classes
        self._subforms = deepcopy(form_instances)
        self._field_name_mapper = {}

        ## Initialize forms if they defined by classes
        for i in range(0, len(self.form_classes)):
            form = self.form_classes[i](data, files)
            self._subforms.append(form)

        ## Fill up the field mapper
        for i in range(0, len(self._subforms)):
            for name in self._subforms[i].fields.keys():
                self._field_name_mapper[name] = i

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