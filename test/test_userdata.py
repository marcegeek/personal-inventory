import personal_inventory.data as dal
from test import Test, make_data_test_users


class TestUserData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.users = make_data_test_users()

    def test_insert(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: usuarios registrados
        for u, user_id in zip(self.users, range(1, len(self.users) + 1)):
            self.assertEqual(u.id, user_id)
        self.assertEqual(len(self.userdao.get_all()), len(self.users))

    def test_update(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: usuarios modificados
        for u in self.users:
            u.firstname = 'Juan'
            self.userdao.update(u)
            self.assertEqual(self.userdao.get_by_id(u.id), u)

    def test_delete(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)
        for u in self.users:
            self.userdao.delete(u.id)

        # post-condiciones: usuarios eliminados
        for u in self.users:
            self.assertIsNone(self.userdao.get_by_id(u.id))
        self.assertEqual(len(self.userdao.get_all()), 0)

    def test_get_by_id(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: recupera usuarios por id
        for u in self.users:
            self.assertEqual(self.userdao.get_by_id(u.id), u)

    def test_get_by_username(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: recupera usuarios por nombre de usuario
        for u in self.users:
            self.assertEqual(self.userdao.get_by_username(u.username), u)

    def test_get_by_email(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: recupera usuarios por e-mail
        for u in self.users:
            self.assertEqual(self.userdao.get_by_email(u.email), u)

    def test_get_by_username_email(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: recupera usuarios por nombre de usuario/e-mail
        for u in self.users:
            self.assertEqual(self.userdao.get_by_username_email(u.username), u)
            self.assertEqual(self.userdao.get_by_username_email(u.email), u)

    def test_get_all(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        # post-condiciones: recupera todos los usuarios
        self.assertEqual(self.userdao.get_all(), self.users)
