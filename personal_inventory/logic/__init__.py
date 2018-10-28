class ValidationError:

    def __init__(self, field):
        self.field = field


class RequiredFieldError(ValidationError):

    def __init__(self, field):
        super().__init__(field)

    def __str__(self):
        return '{0} is required'.format(self.field)


class RepeatedUniqueField(ValidationError):

    def __init__(self, field):
        super().__init__(field)

    def __str__(self):
        return '{0} is repeated'.format(self.field)
