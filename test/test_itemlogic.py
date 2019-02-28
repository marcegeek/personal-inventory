import itertools

from personal_inventory.business.entities.item import Item
from personal_inventory.business.logic import RequiredFieldError, ForeignKeyError, InvalidLength, DeleteForeignKeyError, \
    ValidationException
from personal_inventory.business.logic.item_logic import ItemLogic, InvalidValue, RepeatedItemNameError
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.business.logic.user_logic import UserLogic
from test import Test, make_logic_test_users, make_logic_test_locations, make_logic_test_items


class TestItemLogic(Test):

    def setUp(self):
        super().setUp()
        self.ul = UserLogic()
        self.ll = LocationLogic()
        self.il = ItemLogic()
        self.users = make_logic_test_users()
        self.locations = make_logic_test_locations()
        self.items = make_logic_test_items()

    def test_insert(self):
        self._preconditions()

        # ejecuto la lógica
        success = self._insert_all()

        # post-condiciones: ítems registrados
        self.assertTrue(success)
        for item, item_id in zip(self.items, range(1, len(self.items) + 1)):
            self.assertEqual(item.id, item_id)
        self.assertEqual(len(self.il.get_all()), len(self.items))

    def test_update(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()
        success = True
        for item in self.items:
            item.description += ' updated'
            if not self.il.update(item):
                success = False

        # post-condiciones: ítems modificados
        self.assertTrue(success)
        for item in self.items:
            self.assertEqual(self.il.get_by_id(item.id), item)

    def test_delete(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()
        success = True
        for item in self.items:
            if not self.il.delete(item.id):
                success = False
        failure = self.il.delete(self.items[-1].id + 1)

        # post-condiciones: ubicaciones eliminadas
        self.assertTrue(success)
        self.assertFalse(failure)
        self.assertEqual(len(self.il.get_all()), 0)

    def test_get_by_id(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera los ítems por id
        for item in self.items:
            self.assertEqual(self.il.get_by_id(item.id), item)

    def test_get_all(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera todos los ítems
        self.assertEqual(self.il.get_all(), self.items)

    def test_get_all_by_user(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera ítems por usuario
        for u in self.users:
            user_items = [it for it in self.items if it.owner_id == u.id]
            self.assertEqual(self.il.get_all_by_user(u), user_items)

    def test_get_all_by_location(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera ítems por ubicación
        for loc in self.locations:
            loc_items = [it for it in self.items if it.location_id == loc.id]
            self.assertEqual(self.il.get_all_by_location(loc), loc_items)

    def test_rule_required_fields(self):
        required_fields = {'owner_id', 'location_id', 'description'}
        fields_subsets = list(
            itertools.chain.from_iterable(itertools.combinations(required_fields, r)
                                          for r in range(len(required_fields) + 1))
        )
        fields_subsets = [set(fs) for fs in fields_subsets]

        for expected_fields in fields_subsets:
            # ítem con todos los campos requeridos
            item = Item(owner_id=1, location_id=1, description='Item')

            # elimino los campos que no están presentes
            expected_absent_fields = set([f for f in required_fields if f not in expected_fields])
            for field in expected_absent_fields:
                setattr(item, field, None)

            present_fields = self.il.get_present_fields(item)

            errors = []
            # valida regla
            if expected_fields == required_fields:
                self.assertTrue(self.il.rule_required_fields(errors, present_fields))
            else:
                # falta/n campo/s requerido/s
                self.assertFalse(self.il.rule_required_fields(errors, present_fields))
                for e in errors:
                    self.assertIsInstance(e, RequiredFieldError)
                self.assertEqual(set([e.field for e in errors]), expected_absent_fields)
            self.assertEqual(len(errors), len(expected_absent_fields))
            self.assertEqual(set(present_fields), expected_fields)

    def test_rule_owner_user_exists(self):
        self._preconditions()

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)

        # valida regla
        valid = self.items[0]
        errors = []
        self.assertTrue(self.il.rule_owner_user_exists(valid, errors))
        self.assertEqual(len(errors), 0)

        # usuario propietario no existe
        invalid = Item(owner_id=self.users[-1].id + 1)
        self.assertFalse(self.il.rule_owner_user_exists(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], ForeignKeyError)
        self.assertEqual(errors[0].field, 'owner_id')

    def test_rule_location_exists(self):
        self._preconditions()

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)

        # valida regla
        valid = self.items[0]
        errors = []
        self.assertTrue(self.il.rule_location_exists(valid, errors))
        self.assertEqual(len(errors), 0)

        # ubicación no existe
        invalid = Item(location_id=self.locations[-1].id + 1)
        self.assertFalse(self.il.rule_location_exists(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], ForeignKeyError)
        self.assertEqual(errors[0].field, 'location_id')

    def test_rule_unique_description_per_user(self):
        self._preconditions()

        # ejecuto la lógica
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)
        first_user_items = [it for it in self.items if it.owner_id == self.users[0].id]
        self.ll.insert(first_user_items[0])

        # valida regla
        valid = first_user_items[1]
        errors = []
        self.assertTrue(self.il.rule_unique_description_per_user(valid, errors))
        self.assertEqual(len(errors), 0)

        # nombre de ítem repetido para el mismo usuario
        invalid = Item(owner_id=self.users[0].id, description=first_user_items[0].description)
        self.assertFalse(self.il.rule_unique_description_per_user(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], RepeatedItemNameError)
        self.assertEqual(errors[0].field, 'description')

        # nombre de ítem repepetido para otro usuario (valida regla)
        valid = Item(owner_id=self.users[1].id, description=first_user_items[0].description)
        errors = []
        self.assertTrue(self.il.rule_unique_description_per_user(valid, errors))
        self.assertEqual(len(errors), 0)

    def test_rule_description_len_less_than_3(self):
        # valida regla
        valid = Item(description='Las')
        errors = []
        self.assertTrue(self.il.rule_description_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # descripción menor que 3 caracteres
        invalid = Item(description='La')
        self.assertFalse(self.il.rule_description_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'description')

    def test_rule_description_len_greater_than_50(self):
        # valida regla
        valid = Item(description='El gran y enorme ítem que es mucho mejor que todos')
        errors = []
        self.assertTrue(self.il.rule_description_len(valid, errors))
        self.assertEqual(len(errors), 0)

        # descripción mayor que 50 caracteres
        invalid = Item(description='El gran y enorme ítem que es mucho mejor que todoss')
        self.assertFalse(self.il.rule_description_len(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidLength)
        self.assertEqual(errors[0].field, 'description')

    def rule_valid_quantity(self):
        # valida regla
        valid = Item(quantity=1)
        errors = []
        self.assertTrue(self.il.rule_valid_quantity(valid, errors))
        self.assertEqual(len(errors), 0)
        valid = Item(quantity=0)
        self.assertTrue(self.il.rule_valid_quantity(valid, errors))
        self.assertEqual(len(errors), 0)
        valid = Item(quantity='4')
        self.assertTrue(self.il.rule_valid_quantity(valid, errors))
        self.assertEqual(len(errors), 0)

        # número entero negativo
        invalid = Item(quantity=-1)
        self.assertFalse(self.il.rule_valid_quantity(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidValue)
        self.assertEqual(errors[0].field, 'quantity')

        # número no entero
        invalid = Item(quantity=1.1)
        self.assertFalse(self.il.rule_valid_quantity(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidValue)
        self.assertEqual(errors[0].field, 'quantity')

        # valor no numérico
        invalid = Item(quantity='algo')
        self.assertFalse(self.il.rule_valid_quantity(invalid, errors))
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], InvalidValue)
        self.assertEqual(errors[0].field, 'quantity')

    def test_populate_owner(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera ítems con sus respectivos usuarios según corresponda
        for item in self.items:
            found = self.il.get_by_id(item.id)
            self.assertIsNone(found.owner)
            found = self.il.get_by_id(item.id, populate_owner=False)
            self.assertIsNone(found.owner)
            found = self.il.get_by_id(item.id, populate_owner=True)
            self.assertEqual(found.owner, self.ul.get_by_id(found.owner_id))

    def test_populate_location(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera ítems con sus respectivas ubicaciones según corresponda
        for item in self.items:
            found = self.il.get_by_id(item.id)
            self.assertIsNone(found.location)
            found = self.il.get_by_id(item.id, populate_location=False)
            self.assertIsNone(found.location)
            found = self.il.get_by_id(item.id, populate_location=True)
            self.assertEqual(found.location, self.ll.get_by_id(found.location_id))

    def test_populate_user_items(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera usuarios con sus ítems según corresponda
        for u in self.users:
            found = self.ul.get_by_id(u.id)
            self.assertIsNone(found.locations)
            found = self.ul.get_by_id(u.id, populate_items=False)
            self.assertIsNone(found.locations)
            found = self.ul.get_by_id(u.id, populate_items=True)
            self.assertEqual(found.items, self.il.get_all_by_user(found))

    def test_populate_location_items(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()

        # post-condiciones: recupera ubicaciones con sus ítems según corresponda
        for loc in self.locations:
            found = self.ll.get_by_id(loc.id)
            self.assertIsNone(found.items)
            found = self.ll.get_by_id(loc.id, populate_items=False)
            self.assertIsNone(found.items)
            found = self.ll.get_by_id(loc.id, populate_items=True)
            self.assertEqual(found.items, self.il.get_all_by_location(found))

    def test_delete_fk_rules(self):
        self._preconditions()

        # ejecuto la lógica
        self._insert_all()
        # eliminación de usuarios que pueden estar referenciados por ubicaciones y/o ítems
        for u in self.users:
            errors = []
            if not self.ll.get_all_by_user(u) and not self.il.get_all_by_user(u):
                # no referenciado, se puede eliminar
                self.assertTrue(self.ul.validate_deletion_fk_rules(u.id, errors))
                self.assertEqual(len(errors), 0)
                self.assertTrue(self.ul.delete(u.id))
            else:
                # referenciado, no se puede eliminar
                self.assertFalse(self.ul.validate_deletion_fk_rules(u.id, errors))
                self.assertEqual(len(errors), 1)
                self.assertIsInstance(errors[0], DeleteForeignKeyError)
                self.assertEqual(errors[0].relationship, 'locations')
                with self.assertRaises(ValidationException):
                    self.ul.delete(u.id)
        # eliminación de ubicaciones que pueden estar referenciadas por ítems
        for loc in self.locations:
            errors = []
            if not self.il.get_all_by_location(loc):
                # no referenciada, se puede eliminar
                self.assertTrue(self.ll.validate_deletion_fk_rules(loc.id, errors))
                self.assertEqual(len(errors), 0)
                self.assertTrue(self.ll.delete(loc.id))
            else:
                # referenciada, no se puede eliminar
                self.assertFalse(self.ll.validate_deletion_fk_rules(loc.id, errors))
                self.assertEqual(len(errors), 1)
                self.assertIsInstance(errors[0], DeleteForeignKeyError)
                self.assertEqual(errors[0].relationship, 'items')
                with self.assertRaises(ValidationException):
                    self.ll.delete(loc.id)
        for item in self.items:
            self.il.delete(item.id)
        # ahora sí permite eliminar las ubicaciones que estaban referenciadas
        for loc in self.ll.get_all():
            self.assertTrue(self.ll.delete(loc.id))
        # ahora sí permite eliminar los usuarios que estaban referenciados
        for u in self.ul.get_all():
            self.assertTrue(self.ul.delete(u.id))

        # post-condiciones: igual que al principio
        self._preconditions()

    def _preconditions(self):
        # pre-condiciones: no hay usuarios, ubicaciones, ni ítems registrados
        self.assertEqual(len(self.ul.get_all()), 0)
        self.assertEqual(len(self.ll.get_all()), 0)
        self.assertEqual(len(self.il.get_all()), 0)

    def _insert_all(self):
        success = True
        for u in self.users:
            self.ul.insert(u)
        for loc in self.locations:
            self.ll.insert(loc)
        for item in self.items:
            if not self.il.insert(item):
                success = False
        return success
