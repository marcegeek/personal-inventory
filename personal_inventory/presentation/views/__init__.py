import functools

import flask as fl

from personal_inventory.business.logic import ValidationException
from personal_inventory.presentation.views import error_handler


def business_exception_handler(form):
    """
    Decorator para manejar excepciones de negocio y
    cargar los mensajes en el formulario.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationException as ex:
                for err in ex.args:
                    msg = error_handler.error_str(err)
                    if hasattr(err, 'field') and err.field in form:
                        form[err.field].errors.append(msg)
                    else:
                        form.global_errors.append(msg)

        return wrapper

    return decorator


def _retrieve_last_form(forms):
    if 'last_form' in fl.session:
        last_form = fl.session.pop('last_form')
        for form_key in forms:
            if last_form['key'] == form_key:
                forms[form_key].errors = last_form['errors']
                form_data = last_form['data']
                if forms[form_key].field_errors:
                    for field in form_data:
                        forms[form_key][field].data = form_data[field]


def _save_last_form(form, key):
    fl.session['last_form'] = {
        'key': key,
        'errors': form.errors,
        'data': form.data
    }
