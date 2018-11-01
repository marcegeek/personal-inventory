from personal_inventory.data.models import User, Location
import personal_inventory.data.data as dal
from test import Test


class TestLocationData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.locationdao = dal.LocationData()

    def test_insert(self):
        # pre-condiciones: no hay ubicaciones registradas
        self.assertEqual(len(self.locationdao.get_all()), 0)

        u = User(firstname='Carlos', lastname='García',
                 email='carlosgarcia@gmail.com', username='carlosgarcia',
                 password='123456')
        self.userdao.insert(u)
        loc1 = Location(owner_id=u.id, description='root 1')
        loc2 = Location(owner_id=u.id, description='root 2')
        self.locationdao.insert(loc1)
        self.locationdao.insert(loc2)

        self.assertEqual(loc1.id, 1)
        self.assertEqual(loc2.id, 2)
        self.assertEqual(len(u.locations), 2)
