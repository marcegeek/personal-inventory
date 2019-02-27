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
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        # ejecuto la lógica
        successes = []
        for u in self.users:
            successes.append(self.ul.insert(u))

        # post-condiciones: usuarios registrados
        self.assertEqual(successes, [True] * len(self.users))
        self.assertEqual(len(self.ul.get_all()), len(self.users))

    def test_update(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        # ejecuto la lógica
        successes = []
        for u in self.users:
            self.ul.insert(u)
        for u in self.users:
            u.password = 'algomejor123456'
            successes.append(self.ul.update(u))

        # post-condiciones: usuarios modificados
        self.assertEqual(successes, [True] * len(self.users))
        for u in self.users:
            self.assertEqual(self.ul.get_by_id(u.id), u)

    def test_delete(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        # ejecuto la lógica
        successes = []
        for u in self.users:
            self.ul.insert(u)
        for u in self.users:
            successes.append(self.ul.delete(u.id))
        failure = self.ul.delete(self.users[-1].id + 1)

        # post-condiciones: usuarios eliminados
        self.assertEqual(successes, [True] * len(self.users))
        self.assertFalse(failure)
        self.assertEqual(len(self.ul.get_all()), 0)

    def test_gets(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)

        # post-condiciones: recupera los usuarios
        for u in self.users:
            self.assertEqual(self.ul.get_by_id(u.id), u)
            self.assertEqual(self.ul.get_by_email(u.email), u)
            self.assertEqual(self.ul.get_by_username(u.username), u)
            self.assertEqual(self.ul.get_by_username_email(u.username), u)
            self.assertEqual(self.ul.get_by_username_email(u.email), u)
        # lista ordenada con el orden por defecto
        self.assertEqual(self.ul.get_all(), self.users)

    def test_rule_required_fields(self):
        required_fields = {'firstname', 'lastname', 'email', 'username', 'password'}
        fields_subsets = list(
            itertools.chain.from_iterable(itertools.combinations(required_fields, r)
                                          for r in range(len(required_fields) + 1))
        )
        fields_subsets = [set(fs) for fs in fields_subsets]

        for expected_fields in fields_subsets:
            errors = []
            # usuario con todos los campos requeridos
            user = User(firstname='Juan', lastname='García',
                        email='juangarcia@gmail.com', username='juangarcia',
                        password='123456')
            # elimino los campos que no están presentes
            expected_absent_fields = set([f for f in required_fields if f not in expected_fields])
            for field in expected_absent_fields:
                setattr(user, field, None)
            present_fields = self.ul.get_present_fields(user)
            # valida regla
            if expected_fields == required_fields:
                self.assertTrue(self.ul.rule_required_fields(errors, present_fields))
            else:
                # falta/n campo/s requerido/s
                self.assertFalse(self.ul.rule_required_fields(errors, present_fields))
                for e in errors:
                    self.assertIsInstance(e, RequiredFieldError)
                self.assertEqual(set([e.field for e in errors]), expected_absent_fields)
            self.assertEqual(len(errors), len(expected_absent_fields))
            self.assertEqual(set(present_fields), expected_fields)

    def test_rule_unique_email(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        # ejecuto la lógica
        self.ul.insert(self.users[0])

        # valida regla
        valido = self.users[1]
        errors = []
        self.assertTrue(self.ul.rule_unique_email(valido, errors))
        self.assertEqual(len(errors), 0)

        # e-mail repetido
        invalido = User(firstname='Carlos', lastname='Pérez',
                        email=self.users[0].email, username='carlitos',
                        password='123456')
        self.assertFalse(self.ul.rule_unique_email(invalido, errors))
        self.assertIsInstance(errors[0], RepeatedEmailError)

    def test_rule_unique_username(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        # ejecuto la lógica
        self.ul.insert(self.users[0])

        # valida regla
        valido = self.users[1]
        errors = []
        self.assertTrue(self.ul.rule_unique_username(valido, errors))

        # nombre de usuario repetido
        invalido = User(firstname='Carlos', lastname='Pérez',
                        email='carlitosperez@gmail.com', username=self.users[0].username,
                        password='123456')
        self.assertFalse(self.ul.rule_unique_username(invalido, errors))
        self.assertIsInstance(errors[0], RepeatedUsernameError)

    def test_rule_firstname_len_less_than_2(self):
        # valida regla
        user = User(firstname='Al')
        errors = []
        self.assertTrue(self.ul.rule_firstname_len(user, errors))
        self.assertEqual(len(errors), 0)

        # nombre menor que 2 caracteres
        user = User(firstname='A')
        self.assertFalse(self.ul.rule_firstname_len(user, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'firstname')

    def test_rule_firstname_len_greater_than_40(self):
        # valida regla
        valido = User(firstname='Johann Sebastian Aaaaaaaaaaaaaaaaaaaaaaa')
        errors = []
        self.assertTrue(self.ul.rule_firstname_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # nombre mayor que 40 caracteres
        invalido = User(firstname='Johann Sebastian Aaaaaaaaaaaaaaaaaaaaaaas')
        self.assertFalse(self.ul.rule_firstname_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'firstname')

    def test_rule_lastname_len_less_than_2(self):
        # valida regla
        valido = User(lastname='Bo')
        errors = []
        self.assertTrue(self.ul.rule_lastname_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # apellido menor que 2 caracteres
        invalido = User(lastname='B')
        self.assertFalse(self.ul.rule_lastname_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'lastname')

    def test_rule_lastname_len_greater_than_40(self):
        # valida regla
        valido = User(lastname='Mastropieroooooooooooooooooooooooooooooo')
        errors = []
        self.assertTrue(self.ul.rule_lastname_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # apellido mayor que 15 caracteres
        invalido = User(lastname='Mastropieroooooooooooooooooooooooooooooos')
        self.assertFalse(self.ul.rule_lastname_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'lastname')

    def test_rule_email_len_less_than_3(self):
        # valida regla
        valido = User(email='a@b')
        errors = []
        self.assertTrue(self.ul.rule_email_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # e-mail menor que 3 caracteres
        invalido = User(email='a@')
        self.assertFalse(self.ul.rule_email_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_email_len_greater_than_50(self):
        # valida regla
        valido = User(email='gytwaehwkidtuywxdmxyegiixtkfwvfdjgixifzj@gmail.com')
        errors = []
        self.assertTrue(self.ul.rule_email_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # e-mail mayor que 50 caracteres
        invalido = User(email='gytwaehwkidtuywxdmxyegiixtkfwvfdjgixifzj1@gmail.com')
        self.assertFalse(self.ul.rule_email_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_valid_email(self):
        # valida regla
        valido = User(email='sdfxs.afaf_afa+33@domain.com')
        errors = []
        self.assertTrue(self.ul.rule_valid_email(valido, errors))
        self.assertEqual(len(errors), 0)

        # e-mail con formato inválido
        invalido = User(email='sdfxs.afaf_afa+33.@domain.com')
        self.assertFalse(self.ul.rule_valid_email(invalido, errors))
        self.assertIsInstance(errors[0], InvalidEmailError)
        self.assertEqual(errors[0].field, 'email')

    def test_rule_username_len_less_than_5(self):
        # valida regla
        valido = User(username='admin')
        errors = []
        self.assertTrue(self.ul.rule_username_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # nombre de usuario menor que 5 caracteres
        invalido = User(username='admi')
        self.assertFalse(self.ul.rule_username_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_username_len_greater_than_50(self):
        # valida regla
        valido = User(username='fbeumyivwzzxzrigiuhijhhacvjkncgzpvfnctaubxjlhmffcb')
        errors = []
        self.assertTrue(self.ul.rule_username_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # nombre de usuario mayor que 50 caracteres
        invalido = User(username='fbeumyivwzzxzrigiuhijhhacvjkncgzpvfnctaubxjlhmffcbc')
        self.assertFalse(self.ul.rule_username_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_valid_username(self):
        # valida regla
        valido = User(username='admin1234_dbzdsfe')
        errors = []
        self.assertTrue(self.ul.rule_valid_username(valido, errors))
        self.assertEqual(len(errors), 0)

        # formato de nombre de usuario inválido
        invalido = User(username='asdsfasf3432*')
        self.assertFalse(self.ul.rule_valid_username(invalido, errors))
        self.assertIsInstance(errors[0], InvalidUsernameError)
        self.assertEqual(errors[0].field, 'username')

        # formato de nombre de usuario inválido
        invalido = User(username='afasdf_-sfsf_3432')
        errors = []
        self.assertFalse(self.ul.rule_valid_username(invalido, errors))
        self.assertIsInstance(errors[0], InvalidUsernameError)
        self.assertEqual(errors[0].field, 'username')

    def test_rule_password_len_less_than_6(self):
        # valida regla
        valido = User(password='123456')
        errors = []
        self.assertTrue(self.ul.rule_password_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # contraseña menor que 6 caracteres
        invalido = User(password='12345')
        self.assertFalse(self.ul.rule_password_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'password')

    def test_rule_password_len_greater_than_30(self):
        # valida regla
        valido = User(password='rixrbeggtviybiavhotaegkznidjtq')
        errors = []
        self.assertTrue(self.ul.rule_password_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # contraseña mayor que 30 caracteres
        invalido = User(password='rixrbeggtviybiavhotaegkznidjtqx')
        self.assertFalse(self.ul.rule_password_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'password')
