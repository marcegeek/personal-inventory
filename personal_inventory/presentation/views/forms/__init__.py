import abc

from flask_babel import lazy_gettext as _
from wtforms import Form


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

        def render_field(self, field, render_kw):
            # para que los errores de campo requerido
            # se generen siempre desde las vistas
            render_kw.setdefault('required', False)
            return super().render_field(field, render_kw)

    def __init__(self, formdata=None):
        from personal_inventory.presentation import get_language
        super().__init__(formdata=formdata, meta={'locales': [get_language()]})
        for k in self._fields:
            self._fields[k].mark_required = False
        self.required_msg = _('Fields marked with an asterisk (*) are required')
        self.global_errors = []

    @abc.abstractmethod
    def fill_form(self, obj):
        pass

    @abc.abstractmethod
    def make_object(self, **kwargs):
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
    def fill_form(self, obj):
        pass

    def make_object(self):
        pass

    def update_object(self, obj):
        pass
