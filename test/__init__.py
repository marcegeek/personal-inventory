import unittest

import personal_inventory.data as dal
import personal_inventory.defaultconfigs as config
from personal_inventory.data import UserModel, LocationModel, ItemModel


class Test(unittest.TestCase):

    def setUp(self):
        super().setUp()
        # configurar entorno de prueba: db en memoria
        # la db se resetea con cada test
        dal.configure(config.MemoryDataConfig)


def make_data_test_users():
    return [UserModel(firstname='Carlos', lastname='Pérez',
                      email='carlosperez@gmail.com', username='carlosperez',
                      password='123456'),
            UserModel(firstname='Roberto', lastname='García',
                      email='robgarcia@gmail.com', username='robgarcia',
                      password='123456')]


def make_data_test_locations():
    return [LocationModel(owner_id=1, description='root 1'),
            LocationModel(owner_id=1, description='root 2'),
            LocationModel(owner_id=2, description='root 3'),
            LocationModel(owner_id=2, description='root 4')]


def make_data_test_items():
    return [ItemModel(owner_id=1, location_id=1, description='item 1'),
            ItemModel(owner_id=1, location_id=1, description='item 2'),
            ItemModel(owner_id=1, location_id=2, description='item 3'),
            ItemModel(owner_id=1, location_id=2, description='item 4'),
            ItemModel(owner_id=2, location_id=3, description='item 5'),
            ItemModel(owner_id=2, location_id=3, description='item 6'),
            ItemModel(owner_id=2, location_id=4, description='item 7'),
            ItemModel(owner_id=2, location_id=4, description='item 8')]
