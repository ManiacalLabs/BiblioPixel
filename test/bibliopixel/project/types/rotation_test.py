from . base import TypesBaseTest
from bibliopixel.layout.geometry.rotation import Rotation


class RotationTypesTest(TypesBaseTest):
    def test_some(self):
        self.make('rotation', 'ROTATE_0')
        self.make('rotation', 'ROTATE_90')
        self.make('rotation', 'ROTATE_180')
        self.make('rotation', 'ROTATE_270')

        self.make('rotation', 0, Rotation.ROTATE_0)
        self.make('rotation', 90, Rotation.ROTATE_90)
        self.make('rotation', 180, Rotation.ROTATE_180)
        self.make('rotation', 270, Rotation.ROTATE_270)

        self.make('rotation', 0, Rotation.ROTATE_0)
        self.make('rotation', 1, Rotation.ROTATE_270)
        self.make('rotation', 2, Rotation.ROTATE_180)
        self.make('rotation', 3, Rotation.ROTATE_90)

        with self.assertRaises(KeyError):
            self.make('rotation', 10)

        with self.assertRaises(KeyError):
            self.make('rotation', 'NONE')
