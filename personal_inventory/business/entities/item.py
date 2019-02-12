from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.itemmodel import ItemModel


class Item(BusinessEntity):

    def __init__(self, id=None, owner_id=None, description=None, location_id=None, quantity=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description
        self.location_id = location_id
        self.quantity = quantity
        self.owner = None
        self.location = None

    @classmethod
    def make_from_model(cls, itemmodel, **fill_relations):
        """
        Generar un objeto ítem de negocio a partir del modelo.

        :type itemmodel: ItemModel | list of Item
        :rtype: Item | list of Item
        """
        if itemmodel is None:
            return None
        if isinstance(itemmodel, list):
            return [cls.make_from_model(im, **fill_relations) for im in itemmodel]
        item = cls(itemmodel.id, itemmodel.owner_id, itemmodel.description,
                   itemmodel.location_id, itemmodel.quantity)
        if fill_relations.get('fill_owner', False):
            from personal_inventory.business.entities.user import User
            item.owner = User.make_from_model(itemmodel.owner)
        if fill_relations.get('fill_location', False):
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

        :type itemmodel: ItemModel
        """
        itemmodel.owner_id = self.owner_id
        itemmodel.description = self.description
        itemmodel.location_id = self.location_id
        itemmodel.quantity = self.quantity
