import unittest

import personal_inventory.data.data as dal
import personal_inventory.defaultconfigs as config


class Test(unittest.TestCase):

    def setUp(self):
        super().setUp()
        # configurar entorno de prueba: db en memoria
        # la db se resetea cada vez
        dal.configure(config.MemoryDataConfig)
