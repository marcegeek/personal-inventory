import personal_inventory.data.data as dal
from personal_inventory.data.models.itemmodel import ItemModel
from personal_inventory.data.models.locationmodel import LocationModel
from personal_inventory.data.models.usermodel import UserModel
from test import Test


class TestItemData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.locationdao = dal.LocationData()
        self.itemdao = dal.ItemData()

    def test_insert(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc = LocationModel(owner_id=u.id, description='root 1')
        self.locationdao.insert(loc)

        item1 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 1')
        item2 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 2')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)

        self.assertEqual(item1.id, 1)
        self.assertEqual(item2.id, 2)
        self.assertEqual(self.itemdao.get_all(), [item1, item2])

    def test_update(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc = LocationModel(owner_id=u.id, description='root 1')
        self.locationdao.insert(loc)

        item1 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 1')
        item2 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 2')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)
        item2.description = 'object 2'
        self.itemdao.update(item2)

        self.assertEqual(self.itemdao.get_by_id(item2.id).description, 'object 2')

    def test_delete(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc = LocationModel(owner_id=u.id, description='root 1')
        self.locationdao.insert(loc)

        item1 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 1')
        item2 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 2')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)

        self.itemdao.delete(item1.id)
        self.assertIsNone(self.itemdao.get_by_id(item1.id))
        self.itemdao.delete(item2.id)
        self.assertIsNone(self.itemdao.get_by_id(item2.id))

        self.assertEqual(len(self.itemdao.get_all()), 0)

    def test_get_by_id(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc = LocationModel(owner_id=u.id, description='root 1')
        self.locationdao.insert(loc)

        item1 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 1')
        item2 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 2')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)

        self.assertEqual(self.itemdao.get_by_id(item1.id), item1)
        self.assertEqual(self.itemdao.get_by_id(item2.id), item2)

    def test_get_all(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc = LocationModel(owner_id=u.id, description='root 1')
        self.locationdao.insert(loc)

        item1 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 1')
        item2 = ItemModel(owner_id=u.id, location_id=loc.id, description='item 2')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)

        self.assertEqual(self.itemdao.get_all(), [item1, item2])

    def test_get_all_by_user(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u1 = UserModel(firstname='Carlos', lastname='García',
                       email='carlosgarcia@gmail.com', username='carlosgarcia',
                       password='123456')
        u2 = UserModel(firstname='Carlos G', lastname='Pérez',
                       email='carlosperez@gmail.com', username='carlosperez',
                       password='123456')
        self.userdao.insert(u1)
        self.userdao.insert(u2)
        loc1 = LocationModel(owner_id=u1.id, description='root 1')
        loc2 = LocationModel(owner_id=u2.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        item1 = ItemModel(owner_id=u1.id, location_id=loc1.id, description='item 1')
        item2 = ItemModel(owner_id=u1.id, location_id=loc1.id, description='item 2')
        item3 = ItemModel(owner_id=u2.id, location_id=loc2.id, description='item 3')
        item4 = ItemModel(owner_id=u2.id, location_id=loc2.id, description='item 4')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)
        self.itemdao.insert(item3)
        self.itemdao.insert(item4)

        self.assertEqual(self.itemdao.get_all_by_user(u1), [item1, item2])
        self.assertEqual(self.itemdao.get_all_by_user(u2), [item3, item4])

    def test_get_all_by_location(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        u1 = UserModel(firstname='Carlos', lastname='García',
                       email='carlosgarcia@gmail.com', username='carlosgarcia',
                       password='123456')
        u2 = UserModel(firstname='Carlos G', lastname='Pérez',
                       email='carlosperez@gmail.com', username='carlosperez',
                       password='123456')
        self.userdao.insert(u1)
        self.userdao.insert(u2)
        loc1 = LocationModel(owner_id=u1.id, description='root 1')
        loc2 = LocationModel(owner_id=u2.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        item1 = ItemModel(owner_id=u1.id, location_id=loc1.id, description='item 1')
        item2 = ItemModel(owner_id=u1.id, location_id=loc1.id, description='item 2')
        item3 = ItemModel(owner_id=u2.id, location_id=loc2.id, description='item 3')
        item4 = ItemModel(owner_id=u2.id, location_id=loc2.id, description='item 4')
        self.itemdao.insert(item1)
        self.itemdao.insert(item2)
        self.itemdao.insert(item3)
        self.itemdao.insert(item4)

        self.assertEqual(self.itemdao.get_all_by_location(loc1), [item1, item2])
        self.assertEqual(self.itemdao.get_all_by_location(loc2), [item3, item4])
