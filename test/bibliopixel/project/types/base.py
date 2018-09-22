import unittest
from bibliopixel.project import fields


class TypesBaseTest(unittest.TestCase):
    def make(self, name, c, result=None):
        component = fields.component({name: c}, field_types=fields.FIELD_TYPES)
        if result is not None:
            self.assertEqual(component, {name: result})
        return component
