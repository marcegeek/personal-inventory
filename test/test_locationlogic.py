import itertools

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic import RequiredFieldError, ForeignKeyError, InvalidLength
from personal_inventory.business.logic.location_logic import LocationLogic, RepeatedLocationNameError
from personal_inventory.business.logic.user_logic import UserLogic
from test import Test, make_logic_test_users, make_logic_test_locations


class TestLocationLogic(Test):

    def setUp(self):
        super().setUp()
        self.ul = UserLogic()
        self.ll = LocationLogic()
        self.users = make_logic_test_users()
        self.locations = make_logic_test_locations()

    def test_insert(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        successes = []
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            successes.append(self.ll.insert(loc))

        # post-condiciones: ubicaciones registradas
        self.assertEqual(successes, [True] * len(self.locations))
        for loc, loc_id in zip(self.locations, range(1, len(self.locations) + 1)):
            self.assertEqual(loc.id, loc_id)
        self.assertEqual(len(self.ll.get_all()), len(self.locations))

    def test_update(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        successes = []
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)
        for loc in self.locations:
            loc.description += ' updated'
            successes.append(self.ll.update(loc))

        # post-condiciones: ubicaciones modificadas
        self.assertEqual(successes, [True] * len(self.locations))
        for loc in self.locations:
            self.assertEqual(self.ll.get_by_id(loc.id), loc)

    def test_delete(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        successes = []
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)
        for loc in self.locations:
            successes.append(self.ll.delete(loc.id))
        failure = self.ll.delete(self.locations[-1].id + 1)

        # post-condiciones: ubicaciones eliminadas
        self.assertEqual(successes, [True] * len(self.locations))
        self.assertFalse(failure)
        self.assertEqual(len(self.ll.get_all()), 0)

    def test_gets(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)

        # post-condiciones: recupera las ubicaciones
        for loc in self.locations:
            self.assertEqual(self.ll.get_by_id(loc.id), loc)
        for u in self.users:
            user_locations = [l for l in self.locations if l.owner_id == u.id]
            self.assertEqual(self.ll.get_all_by_user(u), user_locations)
        self.assertEqual(self.ll.get_all(), self.locations)

    def test_rule_required_fields(self):
        required_fields = {'owner_id', 'description'}
        fields_subsets = list(
            itertools.chain.from_iterable(itertools.combinations(required_fields, r)
                                          for r in range(len(required_fields) + 1))
        )
        fields_subsets = [set(fs) for fs in fields_subsets]

        for expected_fields in fields_subsets:
            # ubicación con todos los campos requeridos
            loc = Location(owner_id=1, description='Location')

            # elimino los campos que no están presentes
            expected_absent_fields = set([f for f in required_fields if f not in expected_fields])
            for field in expected_absent_fields:
                setattr(loc, field, None)

            present_fields = self.ll.get_present_fields(loc)

            errors = []
            # valida regla
            if expected_fields == required_fields:
                self.assertTrue(self.ll.rule_required_fields(errors, present_fields))
            else:
                # falta/n campo/s requerido/s
                self.assertFalse(self.ll.rule_required_fields(errors, present_fields))
                for e in errors:
                    self.assertIsInstance(e, RequiredFieldError)
                self.assertEqual(set([e.field for e in errors]), expected_absent_fields)
            self.assertEqual(len(errors), len(expected_absent_fields))
            self.assertEqual(set(present_fields), expected_fields)

    def test_rule_owner_user_exists(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)

        # valida regla
        valid = self.locations[0]
        errors = []
        self.assertTrue(self.ll.rule_owner_user_exists(valid, errors))
        self.assertEqual(len(errors), 0)

        # usuario propietario no existe
        invalid = Location(owner_id=self.users[-1].id + 1, description='Location')
        self.assertFalse(self.ll.rule_owner_user_exists(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], ForeignKeyError)
        self.assertEqual(errors[0].field, 'owner_id')

    def test_rule_unique_description_per_user(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)
        first_user_locations = [l for l in self.locations if l.owner_id == self.users[0].id]
        self.ll.insert(first_user_locations[0])

        # valida regla
        valid = first_user_locations[1]
        errors = []
        self.assertTrue(self.ll.rule_unique_description_per_user(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre de ubicación repetida para el mismo usuario
        invalid = Location(owner_id=self.users[0].id, description=first_user_locations[0].description)
        self.assertFalse(self.ll.rule_unique_description_per_user(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RepeatedLocationNameError)
        self.assertEqual(errors[0].field, 'description')

        # nombre de ubicación repepetida para otro usuario (valida regla)
        valid = Location(owner_id=self.users[1].id, description=first_user_locations[0].description)
        errors = []
        self.assertTrue(self.ll.rule_unique_description_per_user(valid, errors))
        self.assertEqual(len(errors), 0)

    def test_rule_description_len_less_than_3(self):
        # valida regla
        loc = Location(description='Las')
        errors = []
        self.assertTrue(self.ll.rule_description_len(loc, errors))
        self.assertEqual(len(errors), 0)

        # descripción menor que 3 caracteres
        loc = Location(description='La')
        self.assertFalse(self.ll.rule_description_len(loc, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'description')

    def test_rule_description_len_greater_than_50(self):
        # valida regla
        loc = Location(description='La gran y enorme ubicación que es superior a todas')
        errors = []
        self.assertTrue(self.ll.rule_description_len(loc, errors))
        self.assertEqual(len(errors), 0)

        # descripción mayor que 50 caracteres
        loc = Location(description='La gran y enorme ubicación que es superior a todass')
        self.assertFalse(self.ll.rule_description_len(loc, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'description')

    def test_relationships(self):
        # pre-condiciones: no hay usuarios ni ubicaciones registradas
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)

        # post-condiciones: recupera ubicaciones con sus relaciones según corresponda
        for loc in self.locations:
            found = self.ll.get_by_id(loc.id)
            self.assertIsNone(found.owner)
            found = self.ll.get_by_id(loc.id, populate_owner=False)
            self.assertIsNone(found.owner)
            found = self.ll.get_by_id(loc.id, populate_owner=True)
            self.assertEqual(found.owner, self.ul.get_by_id(found.owner_id))
        for u in self.users:
            found = self.ul.get_by_id(u.id)
            self.assertIsNone(found.locations)
            found = self.ul.get_by_id(u.id, populate_locations=False)
            self.assertIsNone(found.locations)
            found = self.ul.get_by_id(u.id, populate_locations=True)
            self.assertEqual(found.locations, self.ll.get_all_by_user(found))
