from personal_inventory.data.models import User
from personal_inventory.logic import RequiredFieldError
from personal_inventory.logic.user_logic import UserLogic, RepeatedEmailError, RepeatedUsernameError, \
    InvalidLengthError, InvalidUsernameError, InvalidEmailError
from test import Test


class TestUserLogic(Test):

    def setUp(self):
        super().setUp()
        self.ul = UserLogic()

    def test_insert(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        user = User(firstname='Carlos', lastname='Pérez',
                    email='carlosperez@gmail.com', username='carlosperez',
                    password='123456')
        success = self.ul.insert(user)

        # post-condiciones
        self.assertTrue(success)
        self.assertEqual(len(self.ul.get_all()), 1)

    def test_update(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        user1 = User(firstname='Carlos', lastname='Pérez',
                     email='carlosperez@gmail.com', username='carlosperez',
                     password='123456')
        user2 = User(firstname='Roberto', lastname='García',
                     email='robgarcia@gmail.com', username='rgarcia',
                     password='123456')
        user3 = User(firstname='José', lastname='Duval',
                     email='jduval@gmail.com', username='jduval',
                     password='123456')
        self.ul.insert(user1)
        self.ul.insert(user2)
        self.ul.insert(user3)
        user2.password = 'algomejor123456'
        success = self.ul.update(user2)

        updated = self.ul.get_by_id(user2.id)

        # post-condiciones
        self.assertTrue(success)
        self.assertEqual(updated.id, user2.id)
        self.assertEqual(updated.password, 'algomejor123456')

    def test_delete(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        user1 = User(firstname='Carlos', lastname='Pérez',
                     email='carlosperez@gmail.com', username='carlosperez',
                     password='123456')
        user2 = User(firstname='Roberto', lastname='García',
                     email='robgarcia@gmail.com', username='rgarcia',
                     password='123456')
        user3 = User(firstname='José', lastname='Duval',
                     email='jduval@gmail.com', username='jduval',
                     password='123456')
        self.ul.insert(user1)
        self.ul.insert(user2)
        self.ul.insert(user3)
        success = self.ul.delete(user2.id)
        failure = self.ul.delete(4)

        # post-condiciones
        self.assertTrue(success)
        self.assertFalse(failure)
        self.assertEqual(len(self.ul.get_all()), 2)

    def test_gets(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        user1 = User(firstname='Carlos', lastname='Pérez',
                     email='carlosperez@gmail.com', username='carlosperez',
                     password='123456')
        user2 = User(firstname='Roberto', lastname='García',
                     email='robgarcia@gmail.com', username='rgarcia',
                     password='123456')
        user3 = User(firstname='José', lastname='Duval',
                     email='jduval@gmail.com', username='jduval',
                     password='123456')
        self.ul.insert(user1)
        self.ul.insert(user2)
        self.ul.insert(user3)

        # post-condiciones
        self.assertEqual(self.ul.get_by_id(user1.id), user1)
        self.assertEqual(self.ul.get_by_email(user1.email), user1)
        self.assertEqual(self.ul.get_by_username(user1.username), user1)
        self.assertEqual(self.ul.get_by_username_email(user1.username), user1)
        self.assertEqual(self.ul.get_by_username_email(user1.email), user1)
        self.assertEqual(self.ul.get_by_id(user2.id), user2)
        self.assertEqual(self.ul.get_by_email(user2.email), user2)
        self.assertEqual(self.ul.get_by_username(user2.username), user2)
        self.assertEqual(self.ul.get_by_username_email(user2.username), user2)
        self.assertEqual(self.ul.get_by_username_email(user2.email), user2)
        self.assertEqual(len(self.ul.get_all()), 3)

    def test_rule_required_fields(self):
        # valida regla
        valido = User(firstname='Juan', lastname='García',
                      email='juangarcia@gmail.com', username='juangarcia',
                      password='123456')

        errors, present_fields = [], []
        self.assertTrue(self.ul.rule_required_fields(valido, errors, present_fields))
        self.assertEqual(len(errors), 0)
        for field in ['firstname', 'lastname', 'email', 'username', 'password']:
            self.assertIn(field, present_fields)

        # falta nombre
        invalido = User(lastname='García',
                        email='juangarcia@gmail.com', username='juangarcia',
                        password='123456')
        errors, present_fields = [], []
        self.assertFalse(self.ul.rule_required_fields(invalido, errors, present_fields))
        self.assertIsInstance(errors[0], RequiredFieldError)
        self.assertEqual(errors[0].field, 'firstname')
        self.assertNotIn('firstname', present_fields)

        # falta apellido
        invalido = User(firstname='Juan',
                        email='juangarcia@gmail.com', username='juangarcia',
                        password='123456')
        errors, present_fields = [], []
        self.assertFalse(self.ul.rule_required_fields(invalido, errors, present_fields))
        self.assertIsInstance(errors[0], RequiredFieldError)
        self.assertEqual(errors[0].field, 'lastname')
        self.assertNotIn('lastname', present_fields)

        # falta e-mail
        invalido = User(firstname='Juan', lastname='García',
                        username='juangarcia',
                        password='123456')
        errors, present_fields = [], []
        self.assertFalse(self.ul.rule_required_fields(invalido, errors, present_fields))
        self.assertIsInstance(errors[0], RequiredFieldError)
        self.assertEqual(errors[0].field, 'email')
        self.assertNotIn('email', present_fields)

        # falta nombre de usuario
        invalido = User(firstname='Juan', lastname='García',
                        email='juanggarcia@gmail.com',
                        password='123456')
        errors, present_fields = [], []
        self.assertFalse(self.ul.rule_required_fields(invalido, errors, present_fields))
        self.assertIsInstance(errors[0], RequiredFieldError)
        self.assertEqual(errors[0].field, 'username')
        self.assertNotIn('username', present_fields)

        # falta contraseña
        invalido = User(firstname='Juan', lastname='García',
                        email='juanggarcia@gmail.com', username='carlosgarcia')
        errors, present_fields = [], []
        self.assertFalse(self.ul.rule_required_fields(invalido, errors, present_fields))
        self.assertIsInstance(errors[0], RequiredFieldError)
        self.assertEqual(errors[0].field, 'password')
        self.assertNotIn('password', present_fields)

    def test_rule_unique_email(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        user = User(firstname='Carlos', lastname='Pérez',
                    email='carlosperez@gmail.com', username='carlosperez',
                    password='123456')
        self.ul.insert(user)

        # valida regla
        valido = User(id=user.id + 1, firstname='Juan', lastname='García',
                      email='juangarcia@gmail.com', username='juangarcia',
                      password='123456')
        errors = []
        self.assertTrue(self.ul.rule_unique_email(valido, errors))
        self.assertEqual(len(errors), 0)

        # E-mail repetido
        invalido = User(id=valido.id + 1, firstname='Carlos', lastname='Pérez',
                        email='carlosperez@gmail.com', username='carlitos',
                        password='123456')
        self.assertFalse(self.ul.rule_unique_email(invalido, errors))
        self.assertIsInstance(errors[0], RepeatedEmailError)

    def test_rule_unique_username(self):
        # pre-condiciones: no hay usuarios registrados
        self.assertEqual(len(self.ul.get_all()), 0)

        user = User(firstname='Carlos', lastname='Pérez',
                    email='carlosperez@gmail.com', username='carlosperez',
                    password='123456')
        self.ul.insert(user)

        # valida regla
        valido = User(id=user.id + 1, firstname='Juan', lastname='García',
                      email='juangarcia@gmail.com', username='juangarcia',
                      password='123456')
        errors = []
        self.assertTrue(self.ul.rule_unique_username(valido, errors))

        # Nombre de usuario repetido
        invalido = User(id=valido.id + 1, firstname='Carlos', lastname='Pérez',
                        email='carlitosperez@gmail.com', username='carlosperez',
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
        self.assertIsInstance(errors[0], InvalidLengthError)
        self.assertEqual(errors[0].field, 'firstname')

    def test_rule_firstname_len_greater_than_15(self):
        # valida regla
        valido = User(firstname='María Antonieta')
        errors = []
        self.assertTrue(self.ul.rule_firstname_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # nombre mayor que 15 caracteres
        invalido = User(firstname='María Antonietaa')
        self.assertFalse(self.ul.rule_firstname_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
        self.assertEqual(errors[0].field, 'lastname')

    def test_rule_lastname_len_greater_than_15(self):
        # valida regla
        valido = User(lastname='Cenarruzabeitia')
        errors = []
        self.assertTrue(self.ul.rule_lastname_len(valido, errors))
        self.assertEqual(len(errors), 0)

        # apellido mayor que 15 caracteres
        invalido = User(lastname='Cenarruzabeitias')
        self.assertFalse(self.ul.rule_lastname_len(invalido, errors))
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
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
        self.assertIsInstance(errors[0], InvalidLengthError)
        self.assertEqual(errors[0].field, 'password')
