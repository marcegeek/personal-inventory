import functools

from personal_inventory.business.logic import ValidationException
from personal_inventory.presentation import error_handler


def business_exception_handler(form):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationException as ex:
                for err in ex.args:
                    msg = error_handler.error_str(err)
                    if err.field in form:
                        form[err.field].errors.append(msg)
                    else:
                        form.global_errors.append(msg)

        return wrapper

    return decorator
