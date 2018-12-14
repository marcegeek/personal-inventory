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


def _strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
