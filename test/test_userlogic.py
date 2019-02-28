import itertools

from personal_inventory.business.entities.user import User
from personal_inventory.business.logic import RequiredFieldError, InvalidLength
from personal_inventory.business.logic.user_logic import UserLogic, RepeatedEmailError, RepeatedUsernameError, \
    InvalidUsernameError, InvalidEmailError
from test import Test, make_logic_test_users


class TestUserLogic(Test):

    def setUp(self):
        super().setUp()
        self.ul = UserLogic()
        self.users = make_logic_test_users()

    def test_insert(self):
        self._preconditions()

        # ejecuto la lógica
        success = self._insert_all()

        # post-condiciones: usuarios registrados
        self.assertTrue(success)
        for u, user_id in zip(self.users, range(1, len(self.users) + 1)):
            self.assertEqual(u.id, user_id)
        self.assertEqual(len(self.ul.get_all()), len(self.users))

    def test_update(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()
        success = True
        for u in self.users:
            u.password = 'algomejor123456'
            if not self.ul.update(u):
                success = False

        # post-condiciones: usuarios modificados
        self.assertTrue(success)
        for u in self.users:
            self.assertEqual(self.ul.get_by_id(u.id), u)

    def test_delete(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()
        success = True
        for u in self.users:
            if not self.ul.delete(u.id):
                success = False
        failure = self.ul.delete(self.users[-1].id + 1)

        # post-condiciones: usuarios eliminados
        self.assertTrue(success)
        self.assertFalse(failure)
        self.assertEqual(len(self.ul.get_all()), 0)

    def test_get_by_id(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera usuarios por id
        for u in self.users:
            self.assertEqual(self.ul.get_by_id(u.id), u)

    def test_get_all(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera todos los usuarios
        self.assertEqual(self.ul.get_all(), self.users)

    def test_get_by_email(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera usuarios por e-mail
        for u in self.users:
            self.assertEqual(self.ul.get_by_email(u.email), u)

    def test_get_by_username(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera usuarios por nombre de usuario
        for u in self.users:
            self.assertEqual(self.ul.get_by_username(u.username), u)

    def test_get_by_username_email(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera usuarios por nombre de usuario/e-mail
        for u in self.users:
            self.assertEqual(self.ul.get_by_username_email(u.username), u)
            self.assertEqual(self.ul.get_by_username_email(u.email), u)

    def test_rule_required_fields(self):
        required_fields = {'firstname', 'lastname', 'email', 'language', 'username', 'password'}
        fields_subsets = list(
            itertools.chain.from_iterable(itertools.combinations(required_fields, r)
                                          for r in range(len(required_fields) + 1))
        )
        fields_subsets = [set(fs) for fs in fields_subsets]

        for expected_fields in fields_subsets:
            # usuario con todos los campos requeridos
            user = User(firstname='Juan', lastname='García',
                        email='juangarcia@gmail.com', language='es',
                        username='juangarcia', password='123456')
            # elimino los campos que no están presentes
            expected_absent_fields = set([f for f in required_fields if f not in expected_fields])
            for field in expected_absent_fields:
                setattr(user, field, None)

            present_fields = self.ul.get_present_fields(user)

            errors = []
            # valida regla
            if expected_fields == required_fields:
                self.assertTrue(self.ul.rule_required_fields(errors, present_fields))
                self.assertEqual(len(errors), 0)
            else:
                # falta/n campo/s requerido/s
                self.assertFalse(self.ul.rule_required_fields(errors, present_fields))
                for e in errors:
                    self.assertIsInstance(e, RequiredFieldError)
                self.assertEqual(set([e.field for e in errors]), expected_absent_fields)
            self.assertEqual(len(errors), len(expected_absent_fields))
            self.assertEqual(set(present_fields), expected_fields)

    def test_rule_unique_email(self):
        self._preconditions()

        # ejecuto la lógica
        self.ul.insert(self.users[0])

        # valida regla
        valid = self.users[1]
        errors = []
        self.assertTrue(self.ul.rule_unique_email(valid, errors))
        self.assertEqual(len(errors), 0)

        # e-mail repetido
        invalid = User(email=self.users[0].email)
        self.assertFalse(self.ul.rule_unique_email(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RepeatedEmailError)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_unique_username(self):
        self._preconditions()

        # ejecuto la lógica
        self.ul.insert(self.users[0])

        # valida regla
        valid = self.users[1]
        errors = []
        self.assertTrue(self.ul.rule_unique_username(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre de usuario repetido
        invalid = User(username=self.users[0].username)
        self.assertFalse(self.ul.rule_unique_username(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RepeatedUsernameError)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_firstname_len_less_than_2(self):
        # valida regla
        valid = User(firstname='Al')
        errors = []
        self.assertTrue(self.ul.rule_firstname_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre menor que 2 caracteres
        invalid = User(firstname='A')
        self.assertFalse(self.ul.rule_firstname_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'firstname')

    def test_rule_firstname_len_greater_than_40(self):
        # valida regla
        valid = User(firstname='Johann Sebastian Aaaaaaaaaaaaaaaaaaaaaaa')
        errors = []
        self.assertTrue(self.ul.rule_firstname_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre mayor que 40 caracteres
        invalid = User(firstname='Johann Sebastian Aaaaaaaaaaaaaaaaaaaaaaas')
        self.assertFalse(self.ul.rule_firstname_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'firstname')

    def test_rule_lastname_len_less_than_2(self):
        # valida regla
        valid = User(lastname='Bo')
        errors = []
        self.assertTrue(self.ul.rule_lastname_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # apellido menor que 2 caracteres
        invalid = User(lastname='B')
        self.assertFalse(self.ul.rule_lastname_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'lastname')

    def test_rule_lastname_len_greater_than_40(self):
        # valida regla
        valid = User(lastname='Mastropieroooooooooooooooooooooooooooooo')
        errors = []
        self.assertTrue(self.ul.rule_lastname_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # apellido mayor que 15 caracteres
        invalid = User(lastname='Mastropieroooooooooooooooooooooooooooooos')
        self.assertFalse(self.ul.rule_lastname_len(invalid, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].field, 'lastname')

    def test_rule_email_len_less_than_3(self):
        # valida regla
        valid = User(email='a@b')
        errors = []
        self.assertTrue(self.ul.rule_email_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # e-mail menor que 3 caracteres
        invalid = User(email='a@')
        self.assertFalse(self.ul.rule_email_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_email_len_greater_than_50(self):
        # valida regla
        valid = User(email='gytwaehwkidtuywxdmxyegiixtkfwvfdjgixifzj@gmail.com')
        errors = []
        self.assertTrue(self.ul.rule_email_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # e-mail mayor que 50 caracteres
        invalid = User(email='gytwaehwkidtuywxdmxyegiixtkfwvfdjgixifzj1@gmail.com')
        self.assertFalse(self.ul.rule_email_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_valid_email(self):
        # valida regla
        valid = User(email='sdfxs.afaf_afa+33@domain.com')
        errors = []
        self.assertTrue(self.ul.rule_valid_email(valid, errors))
        self.assertEqual(len(errors), 0)

        # e-mail con formato inválido
        invalid = User(email='sdfxs.afaf_afa+33.@domain.com')
        self.assertFalse(self.ul.rule_valid_email(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidEmailError)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_username_len_less_than_5(self):
        # valida regla
        valid = User(username='admin')
        errors = []
        self.assertTrue(self.ul.rule_username_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre de usuario menor que 5 caracteres
        invalid = User(username='admi')
        self.assertFalse(self.ul.rule_username_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_username_len_greater_than_50(self):
        # valida regla
        valid = User(username='fbeumyivwzzxzrigiuhijhhacvjkncgzpvfnctaubxjlhmffcb')
        errors = []
        self.assertTrue(self.ul.rule_username_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre de usuario mayor que 50 caracteres
        invalid = User(username='fbeumyivwzzxzrigiuhijhhacvjkncgzpvfnctaubxjlhmffcbc')
        self.assertFalse(self.ul.rule_username_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_valid_username(self):
        # valida regla
        valid = User(username='admin1234_dbzdsfe')
        errors = []
        self.assertTrue(self.ul.rule_valid_username(valid, errors))
        self.assertEqual(len(errors), 0)

        # formato de nombre de usuario inválido
        invalid = User(username='asdsfasf3432*')
        self.assertFalse(self.ul.rule_valid_username(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidUsernameError)
        self.assertEqual(errors[0].field, 'username')

        # formato de nombre de usuario inválido
        invalid = User(username='afasdf_-sfsf_3432')
        errors = []
        self.assertFalse(self.ul.rule_valid_username(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidUsernameError)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_password_len_less_than_6(self):
        # valida regla
        valid = User(password='123456')
        errors = []
        self.assertTrue(self.ul.rule_password_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # contraseña menor que 6 caracteres
        invalid = User(password='12345')
        self.assertFalse(self.ul.rule_password_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'password')

    def test_rule_password_len_greater_than_30(self):
        # valida regla
        valid = User(password='rixrbeggtviybiavhotaegkznidjtq')
        errors = []
        self.assertTrue(self.ul.rule_password_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # contraseña mayor que 30 caracteres
        invalid = User(password='rixrbeggtviybiavhotaegkznidjtqx')
        self.assertFalse(self.ul.rule_password_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'password')

    def _preconditions(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

    def _insert_all(self):
        success = True
        for u in self.users:
            if not self.ul.insert(u):
                success = False
        return success
