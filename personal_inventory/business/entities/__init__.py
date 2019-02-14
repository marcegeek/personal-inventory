import abc


class BusinessEntity(abc.ABC):
    """Entidad de la capa de negocio."""

    def __init__(self, id=None):
        self.id = id

    @classmethod
    @abc.abstractmethod
    def make_from_model(cls, modelobject, **populate_relations):
        pass

    @abc.abstractmethod
    def to_model(self):
        pass

    @abc.abstractmethod
    def update_model(self, modelobject):
        pass
