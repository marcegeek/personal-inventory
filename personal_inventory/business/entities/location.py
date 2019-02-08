from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.locationmodel import LocationModel


class Location(BusinessEntity):

    def __init__(self, id=None, owner_id=None, description=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description
        self.owner = None
        self.items = None

    @classmethod
    def make_from_model(cls, locationmodel, **fill_relations):
        """
        Generar un objeto ubicación de negocio a partir del modelo.

        :type locationmodel: LocationModel | list of LocationModel
        :type fill_relations: dict of bool
        :rtype: Location | list of Location
        """
        if locationmodel is None:
            return None
        if isinstance(locationmodel, list):
            return [cls.make_from_model(lm, **fill_relations) for lm in locationmodel]
        location = cls(locationmodel.id, locationmodel.owner_id, locationmodel.description)
        if fill_relations.get('fill_owner', False):
            from personal_inventory.business.entities.user import User
            location.owner = User.make_from_model(locationmodel.owner)
        if fill_relations.get('fill_items', False):
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

        :type locationmodel: LocationModel
        """
        locationmodel.owner_id = self.owner_id
        locationmodel.description = self.description
