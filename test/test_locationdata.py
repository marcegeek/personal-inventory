import personal_inventory.data as dal
from test import Test, make_data_test_users, make_data_test_locations


class TestLocationData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.locationdao = dal.LocationData()
        self.users = make_data_test_users()
        self.locations = make_data_test_locations()

    def test_insert(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: ubicaciones registradas
        for loc, loc_id in zip(self.locations, range(1, len(self.locations) + 1)):
            self.assertEqual(loc.id, loc_id)
        self.assertEqual(len(self.locationdao.get_all()), len(self.locations))

    def test_update(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: ubicaciones modificadas
        for loc in self.locations:
            loc.description = 'location'
            self.locationdao.update(loc)
            self.assertEqual(self.locationdao.get_by_id(loc.id), loc)

    def test_delete(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: ubicaciones eliminadas
        for loc in self.locations:
            self.locationdao.delete(loc.id)
            self.assertIsNone(self.locationdao.get_by_id(loc.id))
        self.assertEqual(len(self.locationdao.get_all()), 0)

    def test_get_by_id(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: recupera ubicaciones por id
        for loc in self.locations:
            self.assertEqual(self.locationdao.get_by_id(loc.id), loc)

    def test_get_all(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: recupera todas las ubicaciones
        self.assertEqual(self.locationdao.get_all(), self.locations)

    def test_get_all_by_user(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: recupera ubicaciones por usuario
        for u in self.users:
            user_locations = [l for l in self.locations if l.owner_id == u.id]
            self.assertEqual(self.locationdao.get_all_by_user(u), user_locations)

    def test_relationships(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)

        # post-condiciones: recupera las relaciones correspondientes
        for u in self.users:
            user_locations = [l for l in self.locations if l.owner_id == u.id]
            self.assertEqual(u.locations, user_locations)
        for loc in self.locations:
            loc_owner = [u for u in self.users if u.id == loc.owner_id][0]
            self.assertEqual(loc.owner, loc_owner)
