import personal_inventory.data as dal
from personal_inventory.data.models.locationmodel import LocationModel
from personal_inventory.data.models.usermodel import UserModel
from test import Test


class TestLocationData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.locationdao = dal.LocationData()

    def test_insert(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc1 = LocationModel(owner_id=u.id, description='root 1')
        loc2 = LocationModel(owner_id=u.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        self.assertEqual(loc1.id, 1)
        self.assertEqual(loc2.id, 2)
        self.assertEqual(self.locationdao.get_all(), [loc1, loc2])

    def test_update(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc1 = LocationModel(owner_id=u.id, description='root 1')
        loc2 = LocationModel(owner_id=u.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        loc2.description = 'loc 2'
        self.locationdao.update(loc2)
        self.assertEqual(self.locationdao.get_by_id(loc2.id).description, 'loc 2')

    def test_delete(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc1 = LocationModel(owner_id=u.id, description='root 1')
        loc2 = LocationModel(owner_id=u.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        self.locationdao.delete(loc1.id)
        self.assertIsNone(self.locationdao.get_by_id(loc1.id))
        self.locationdao.delete(loc2.id)
        self.assertIsNone(self.locationdao.get_by_id(loc2.id))

        self.assertEqual(len(self.locationdao.get_all()), 0)

    def test_get_by_id(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc1 = LocationModel(owner_id=u.id, description='root 1')
        loc2 = LocationModel(owner_id=u.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        self.assertEqual(self.locationdao.get_by_id(loc1.id), loc1)
        self.assertEqual(self.locationdao.get_by_id(loc2.id), loc2)

    def test_get_all(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u = UserModel(firstname='Carlos', lastname='García',
                      email='carlosgarcia@gmail.com', username='carlosgarcia',
                      password='123456')
        self.userdao.insert(u)
        loc1 = LocationModel(owner_id=u.id, description='root 1')
        loc2 = LocationModel(owner_id=u.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        self.assertEqual(self.locationdao.get_all(), [loc1, loc2])

    def test_get_all_by_user(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u1 = UserModel(firstname='Carlos', lastname='García',
                       email='carlosgarcia@gmail.com', username='carlosgarcia',
                       password='123456')
        u2 = UserModel(firstname='Carlos G', lastname='Pérez',
                       email='carlosperez@gmail.com', username='carlosperez',
                       password='123456')
        self.userdao.insert(u1)
        self.userdao.insert(u2)
        loc1 = LocationModel(owner_id=u1.id, description='root 1')
        loc2 = LocationModel(owner_id=u1.id, description='root 2')
        loc3 = LocationModel(owner_id=u2.id, description='root 3')
        loc4 = LocationModel(owner_id=u2.id, description='root 4')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)
        self.locationdao.insert(loc3)
        self.locationdao.insert(loc4)

        self.assertEqual(self.locationdao.get_all_by_user(u1), [loc1, loc2])
        self.assertEqual(self.locationdao.get_all_by_user(u2), [loc3, loc4])

    def test_relationships(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u1 = UserModel(firstname='Carlos', lastname='García',
                       email='carlosgarcia@gmail.com', username='carlosgarcia',
                       password='123456')
        u2 = UserModel(firstname='Carlos G', lastname='Pérez',
                       email='carlosperez@gmail.com', username='carlosperez',
                       password='123456')
        self.userdao.insert(u1)
        self.userdao.insert(u2)
        loc1 = LocationModel(owner_id=u1.id, description='root 1')
        loc2 = LocationModel(owner_id=u1.id, description='root 2')
        loc3 = LocationModel(owner_id=u2.id, description='root 3')
        loc4 = LocationModel(owner_id=u2.id, description='root 4')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)
        self.locationdao.insert(loc3)
        self.locationdao.insert(loc4)

        self.assertEqual(u1.locations, [loc1, loc2])
        self.assertEqual(loc1.owner, u1)
        self.assertEqual(loc2.owner, u1)
        self.assertEqual(u2.locations, [loc3, loc4])
        self.assertEqual(loc3.owner, u2)
        self.assertEqual(loc4.owner, u2)
