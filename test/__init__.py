import unittest

from personal_inventory import config


class Test(unittest.TestCase):

    def setUp(self):
        super().setUp()
        # configurar entorno de prueba: db en memoria
        # la db se resetea cada vez
        config.set_data_enviroment(config.Environment.TESTING)
