import unittest
from bibliopixel.project.types import defaults, make


class TypesBaseTest(unittest.TestCase):
    def make(self, name, c, result=None):
        component = make.component({name: c}, field_types=defaults.FIELD_TYPES)
        if result is not None:
            self.assertEquals(component, {name: result})
        return component
