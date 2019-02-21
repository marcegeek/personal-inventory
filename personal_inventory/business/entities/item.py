import functools
import locale

from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.itemmodel import ItemModel


@functools.total_ordering
class Item(BusinessEntity):
    """Entidad ítem de la capa de negocio."""

    def __init__(self, id=None, owner_id=None, description=None, location_id=None, quantity=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description
        self.location_id = location_id
        self.quantity = quantity
        self.owner = None
        self.location = None

    def __eq__(self, other):
        o1 = (self.id, self.owner_id, self.description, self.location_id,
              self.quantity, self.owner, self.location)
        o2 = (other.id, other.owner_id, other.description, other.location_id,
              other.quantity, other.owner, other.location)
        return o1 == o2

    def __lt__(self, other):
        if self.location is not None and other.location is not None:
            o1 = (self.location, locale.strxfrm(self.description))
            o2 = (other.location, locale.strxfrm(other.description))
        else:
            o1 = locale.strxfrm(self.description)
            o2 = locale.strxfrm(other.description)
        return o1 < o2

    @classmethod
    def make_from_model(cls, itemmodel, populate_owner=False, populate_location=False):
        """
        Generar un objeto ítem de negocio a partir del modelo.
        Pudiendo rellenar las relaciones con su propietario y/o su
        ubicación.

        Las relaciones no se rellenan de manera recursiva.

        :type itemmodel: ItemModel | list of Item
        :type populate_owner: bool
        :type populate_location: bool
        :rtype: Item | list of Item
        """
        if itemmodel is None:
            return None
        if isinstance(itemmodel, list):
            items = [cls.make_from_model(im, populate_owner, populate_location) for im in itemmodel]
            items.sort()
            return items
        item = cls(itemmodel.id, itemmodel.owner_id, itemmodel.description,
                   itemmodel.location_id, itemmodel.quantity)
        if populate_owner:
            from personal_inventory.business.entities.user import User
            item.owner = User.make_from_model(itemmodel.owner)
        if populate_location:
            from personal_inventory.business.entities.location import Location
            item.location = Location.make_from_model(itemmodel.location)
        return item

    def to_model(self):
        """
        Generar un objeto ítem del modelo desde el objeto de negocio.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: ItemModel
        """
        itemmodel = ItemModel(id=self.id)
        self.update_model(itemmodel)
        return itemmodel

    def update_model(self, itemmodel):
        """
        Modificar un objeto ítem del modelo desde el objeto de negocio.
        El id no se modifica.

        Las relaciones con otros objetos no se modifican.

        :type itemmodel: ItemModel
        """
        itemmodel.owner_id = self.owner_id
        itemmodel.description = self.description
        itemmodel.location_id = self.location_id
        itemmodel.quantity = self.quantity
