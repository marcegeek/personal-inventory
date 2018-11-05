from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.locationmodel import LocationModel


class Location(BusinessEntity):

    def __init__(self, id=None, owner_id=None, description=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description

    @classmethod
    def make_from_model(cls, locationmodel):
        """
        Generar un objeto ubicación de negocio a partir del modelo.

        :type locationmodel: LocationModel
        :rtype: Location
        """
        if locationmodel is None:
            return None
        location = cls(locationmodel.id, locationmodel.owner_id, locationmodel.description)
        return location

    def to_model(self):
        """
        Generar un objeto ubicación del modelo desde el objeto de negocio.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: LocationModel
        """
        return LocationModel(id=self.id, owner_id=self.owner_id,
                             description=self.description)

    def update_model(self, locationmodel):
        """
        Modificar un objeto ubicación del modelo desde el objeto de negocio.
        El id no se modifica.

        :type locationmodel: LocationModel
        """
        locationmodel.owner_id = self.owner_id
        locationmodel.description = self.description
