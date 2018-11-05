from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.usagemodel import UsageModel


class Usage(BusinessEntity):

    def __init__(self, id=None, item_id=None, start_date=None, end_date=None):
        super().__init__(id)
        self.item_id = item_id
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def make_from_model(cls, usagemodel):
        """
        Generar un objeto utilización de negocio a partir del modelo.

        :type usagemodel: UsageModel
        :rtype: Usage
        """
        if usagemodel is None:
            return None
        usage = cls(id=usagemodel.id, start_date=usagemodel.start_date,
                    end_date=usagemodel.end_date)
        return usage

    def to_model(self):
        """
        Generar un objeto utilización del modelo desde el objeto de negocio.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: UsageModel
        """
        usagemodel = UsageModel(id=self.id)
        self.update_model(usagemodel)
        return usagemodel

    def update_model(self, usagemodel):
        """
        Modificar un objeto ítem del modelo desde el objeto de negocio.
        El id no se modifica.

        :type usagemodel: UsageModel
        """
        usagemodel.item_id = self.item_id
        usagemodel.start_date = self.start_date
        usagemodel.end_date = self.end_date
