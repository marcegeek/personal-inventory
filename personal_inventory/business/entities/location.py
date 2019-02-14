from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.locationmodel import LocationModel


class Location(BusinessEntity):
    """Entidad ubicación de la capa de negocio."""

    def __init__(self, id=None, owner_id=None, description=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description
        self.owner = None
        self.items = None

    def __eq__(self, other):
        o1 = (self.id, self.owner_id, self.description, self.owner, self.items)
        o2 = (other.id, other.owner_id, other.description, other.owner, other.items)
        return o1 == o2

    @classmethod
    def make_from_model(cls, locationmodel, populate_owner=False, populate_items=False):
        """
        Generar un objeto ubicación de negocio a partir del modelo.
        Pudiendo rellenar las relaciones con su propietario y/o sus
        ítems.

        Las relaciones no se rellenan de manera recursiva.

        :type locationmodel: LocationModel | list of LocationModel
        :type populate_owner: bool
        :type populate_items: bool
        :rtype: Location | list of Location
        """
        if locationmodel is None:
            return None
        if isinstance(locationmodel, list):
            return [cls.make_from_model(lm, populate_owner, populate_items) for lm in locationmodel]
        location = cls(locationmodel.id, locationmodel.owner_id, locationmodel.description)
        if populate_owner:
            from personal_inventory.business.entities.user import User
            location.owner = User.make_from_model(locationmodel.owner)
        if populate_items:
            from personal_inventory.business.entities.item import Item
            location.items = Item.make_from_model(locationmodel.items)
        return location

    def to_model(self):
        """
        Generar un objeto ubicación del modelo desde el objeto de negocio.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: LocationModel
        """
        locationmodel = LocationModel(id=self.id)
        self.update_model(locationmodel)
        return locationmodel

    def update_model(self, locationmodel):
        """
        Modificar un objeto ubicación del modelo desde el objeto de negocio.
        El id no se modifica.

        Las relaciones con otros objetos no se modifican.

        :type locationmodel: LocationModel
        """
        locationmodel.owner_id = self.owner_id
        locationmodel.description = self.description
