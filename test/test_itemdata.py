import personal_inventory.data as dal
from test import Test, make_data_test_users, make_data_test_locations, make_data_test_items


class TestItemData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.locationdao = dal.LocationData()
        self.itemdao = dal.ItemData()
        self.users = make_data_test_users()
        self.locations = make_data_test_locations()
        self.items = make_data_test_items()

    def test_insert(self):
        self._preconditions()

        self._insert_all()

        # post-condiciones: ítems registrados
        for item, item_id in zip(self.items, range(1, len(self.items) + 1)):
            self.assertEqual(item.id, item_id)

    def test_update(self):
        self._preconditions()

        self._insert_all()

        for item in self.items:
            item.description = 'object'
            self.itemdao.update(item)

        # post-condiciones: ítems modificados
        for item in self.items:
            self.assertEqual(self.itemdao.get_by_id(item.id), item)

    def test_delete(self):
        self._preconditions()

        self._insert_all()

        for item in self.items:
            self.itemdao.delete(item.id)

        # post-condiciones: ítems eliminados
        for item in self.items:
            self.assertIsNone(self.itemdao.get_by_id(item.id))
        self.assertEqual(len(self.itemdao.get_all()), 0)

    def test_get_by_id(self):
        self._preconditions()

        self._insert_all()

        # post-condiciones: recupera ítems por id
        for item in self.items:
            self.assertEqual(self.itemdao.get_by_id(item.id), item)

    def test_get_all(self):
        self._preconditions()

        self._insert_all()

        # post-condiciones: recupera todos los ítems
        self.assertEqual(self.itemdao.get_all(), self.items)

    def test_get_all_by_user(self):
        self._preconditions()

        self._insert_all()

        # post-condiciones: recupera ítems por usuario
        for u in self.users:
            user_items = [item for item in self.items if item.owner_id == u.id]
            self.assertEqual(self.itemdao.get_all_by_user(u), user_items)

    def test_get_all_by_location(self):
        self._preconditions()

        self._insert_all()

        # post-condiciones: recupera ítems por ubicación
        for loc in self.locations:
            loc_items = [item for item in self.items if item.location_id == loc.id]
            self.assertEqual(self.itemdao.get_all_by_location(loc), loc_items)

    def test_relationship_owner(self):
        self._preconditions()

        self._insert_all()

        for item in self.items:
            item_owner = [u for u in self.users if u.id == item.owner_id][0]
            self.assertEqual(item.owner, item_owner)

    def test_relationship_location(self):
        self._preconditions()

        self._insert_all()

        for item in self.items:
            item_loc = [loc for loc in self.locations if loc.id == item.location_id][0]
            self.assertEqual(item.location, item_loc)

    def test_relationship_items_by_user(self):
        self._preconditions()

        self._insert_all()

        for u in self.users:
            user_items = self.itemdao.get_all_by_user(u)
            self.assertEqual(u.items, user_items)

    def test_relationship_items_by_location(self):
        self._preconditions()

        self._insert_all()

        for loc in self.locations:
            loc_items = self.itemdao.get_all_by_location(loc)
            self.assertEqual(loc.items, loc_items)

    def _preconditions(self):
        # pre-condiciones: no hay usuarios, ubicaciones ni ítems registrados
        self.assertEqual(len(self.userdao.get_all()), 0)
        self.assertEqual(len(self.locationdao.get_all()), 0)
        self.assertEqual(len(self.itemdao.get_all()), 0)

    def _insert_all(self):
        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)
