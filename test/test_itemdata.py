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
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        item_id = 1
        for item in self.items:
            self.assertEqual(item.id, item_id)
            item_id += 1

    def test_update(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        for item in self.items:
            item.description = 'object'
            self.itemdao.update(item)
            self.assertEqual(self.itemdao.get_by_id(item.id), item)

    def test_delete(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        for item in self.items:
            self.itemdao.delete(item.id)
            self.assertIsNone(self.itemdao.get_by_id(item.id))
        self.assertEqual(len(self.itemdao.get_all()), 0)

    def test_get_by_id(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        for item in self.items:
            self.assertEqual(self.itemdao.get_by_id(item.id), item)

    def test_get_all(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        self.assertEqual(self.itemdao.get_all(), self.items)

    def test_get_all_by_user(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        for u in self.users:
            user_items = [item for item in self.items if item.owner_id == u.id]
            self.assertEqual(self.itemdao.get_all_by_user(u), user_items)

    def test_get_all_by_location(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        for loc in self.locations:
            loc_items = [item for item in self.items if item.location_id == loc.id]
            self.assertEqual(self.itemdao.get_all_by_location(loc), loc_items)

    def test_relationships(self):
        # pre-condiciones: no hay ítems registrados
        self.assertEqual(len(self.itemdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for loc in self.locations:
            self.locationdao.insert(loc)
        for item in self.items:
            self.itemdao.insert(item)

        for u in self.users:
            user_items = [item for item in self.items if item.owner_id == u.id]
            self.assertEqual(u.items, user_items)
        for loc in self.locations:
            loc_items = [item for item in self.items if item.location_id == loc.id]
            self.assertEqual(loc.items, loc_items)
        for item in self.items:
            item_loc = [loc for loc in self.locations if loc.id == item.location_id][0]
            self.assertEqual(item.location, item_loc)
