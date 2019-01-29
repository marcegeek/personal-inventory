from wtforms import Form


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
        self._errors = None
        self._field_errors = None

    @property
    def errors(self):
        if self._errors is None:
            self._errors = super().errors.copy()
            if self.global_errors:
                self.errors['_global'] = self.global_errors
        return self._errors

    @property
    def field_errors(self):
        return super().errors

    def set_errors(self, errors):
        for field, err in zip(errors.keys(), errors.values()):
            if field != '_global':
                self[field].errors = err
            else:
                self.global_errors = err


def _strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
