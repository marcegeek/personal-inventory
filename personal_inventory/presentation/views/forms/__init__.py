import abc
import functools

from wtforms import Form


def safe_form(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self._ensure_from_ready(**kwargs)
        return func(self, *args, **kwargs)

    return wrapper


def _strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value


class BaseForm(Form):
    class Meta:
        @staticmethod
        def bind_field(form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            filters.append(_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_errors = []

    @abc.abstractmethod
    def ensure_form_ready(self, **kwargs):
        pass

    @safe_form
    @abc.abstractmethod
    def fill_form(self, obj, **kwargs):
        pass

    @abc.abstractmethod
    def make_object(self):
        pass

    @abc.abstractmethod
    def update_object(self, obj):
        pass

    @property
    def errors(self):
        errors = super().errors.copy()
        if self.global_errors:
            errors['_global'] = self.global_errors
        return errors

    @errors.setter
    def errors(self, errors):
        for field, err in zip(errors.keys(), errors.values()):
            if field != '_global':
                self[field].errors = err
            else:
                self.global_errors = err

    @property
    def field_errors(self):
        return super().errors


class DeleteForm(BaseForm):
    def ensure_form_ready(self, **kwargs):
        pass

    def fill_form(self, obj, **kwargs):
        pass

    def make_object(self):
        pass

    def update_object(self, obj):
        pass
