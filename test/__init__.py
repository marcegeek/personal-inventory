import unittest

import personal_inventory.data.data as dal
import config


class Test(unittest.TestCase):

    def setUp(self):
        super().setUp()
        # configurar entorno de prueba: db en memoria
        config.env = config.TESTING
        dal.configure()  # esto inicia una nueva db limpia
