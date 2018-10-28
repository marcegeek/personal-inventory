import unittest

import personal_inventory.data.data as dal
from personal_inventory.data.models import User
from test import Test


class TestUserData(Test):

    def setUp(self):
        super().setUp()
        self.userdao = dal.UserData()
        self.users = [User(firstname='Carlos', lastname='Pérez',
                           email='carlosperez@gmail.com', username='carlosperez',
                           password='123456'),
                      User(firstname='Roberto', lastname='García',
                           email='robgarcia@gmail.com', username='robgarcia',
                           password='123456')]

    def test_insert(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        u = self.users[0]
        self.userdao.insert(u)
        self.assertEqual(u.id, 1)

    def test_update(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        for u in self.users:
            u.firstname = 'Juan'
            self.userdao.update(u)
            found = self.userdao.get_by_id(u.id)
            self.assertEqual(found.firstname, 'Juan')

    def test_delete(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        for u in self.users:
            self.userdao.delete(u.id)
            self.assertIsNone(self.userdao.get_by_id(u.id))

        self.assertEqual(len(self.userdao.get_all()), 0)

    def test_get_by_id(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        for u in self.users:
            self.assertEqual(self.userdao.get_by_id(u.id), u)

    def test_get_by_username(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        for u in self.users:
            self.assertEqual(self.userdao.get_by_username(u.username), u)

    def test_get_by_email(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        for u in self.users:
            self.assertEqual(self.userdao.get_by_email(u.email), u)

    def test_get_by_username_email(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        for u in self.users:
            self.assertEqual(self.userdao.get_by_username_email(u.username), u)
            self.assertEqual(self.userdao.get_by_username_email(u.email), u)

    def test_get_all(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.userdao.get_all()), 0)

        for u in self.users:
            self.userdao.insert(u)

        self.assertEqual(self.userdao.get_all(), self.users)
