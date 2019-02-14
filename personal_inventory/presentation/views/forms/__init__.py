import abc

from flask_babel import lazy_gettext as _
from wtforms import Form
from wtforms.widgets import html_params


def _strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value


class BaseForm(Form):
    """
    Base de los formularios.

    Integra todos los datos para la presentación de los mismos.
    """
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
        self.modal_id = None
        self.title = ''
        self.action = None
        self.method = 'POST'
        self.fields_to_render = []
        self.autofocus_field = None
        self.submit = _('Save')
        self.global_errors = []
        self.required_msg = _('Fields marked with an asterisk (*) are required')
        for k in self._fields:
            self._fields[k].mark_required = False
        self.extra_body_html = None  # trozo de HTML antes (o en lugar) de los campos
        self.extra_footer_html = None  # footer al final del form, solamente si no es modal

    @abc.abstractmethod
    def fill(self, obj):
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

    def __init__(self, formdata=None):
        super().__init__(formdata=formdata)
        self.submit = _('Delete')

    @staticmethod
    def delete_body(object_name):
        html = '<p {}>'.format(html_params(class_='lead'))
        html += _('Do you really want to delete "%(element)s"?', element=object_name)
        html += '</p>\n'
        html += '<p {}>'.format(html_params(class_='text-warning'))
        html += _('This action cannot be undone.')
        html += '</p>'
        return html

    def fill(self, obj):
        pass

    def make_object(self):
        pass

    def update_object(self, obj):
        pass
