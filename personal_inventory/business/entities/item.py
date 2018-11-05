from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.itemmodel import ItemModel


class Item(BusinessEntity):

    def __init__(self, id=None, owner_id=None, description=None, location_id=None, quantity=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description
        self.location_id = location_id
        self.quantity = quantity

    @classmethod
    def make_from_model(cls, itemmodel):
        """
        Generar un objeto ítem de negocio a partir del modelo.

        :type itemmodel: ItemModel
        :return: Item
        """
        if itemmodel is None:
            return None
        item = cls(itemmodel.id, itemmodel.owner_id, itemmodel.description,
                   itemmodel.location_id, itemmodel.quantity)
        return item

    def to_model(self):
        """
        Generar un objeto ítem del modelo desde el objeto de negocio.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: ItemModel
        """
        return ItemModel(id=self.id, owner_id=self.owner_id, location_id=self.location_id,
                         description=self.description, quantity=self.quantity)

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
