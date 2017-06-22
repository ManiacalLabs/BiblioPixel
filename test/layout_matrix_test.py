import unittest
from bibliopixel.layout.geometry import matrix


class MatrixTest(unittest.TestCase):
    def test_simple(self):
        m = matrix.Matrix(list(range(12)), 3)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(1, 0), 1)
        self.assertEqual(m.get(0, 1), 3)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(2, 3), 11)

    def test_transpose(self):
        m = matrix.Matrix(list(range(12)), 3, transpose=True)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(0, 1), 1)
        self.assertEqual(m.get(1, 0), 3)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(3, 2), 11)

    def test_reflect(self):
        m = matrix.Matrix(list(range(12)), 3, reflect_x=True)
        self.assertEqual(m.get(0, 0), 2)
        self.assertEqual(m.get(1, 0), 1)
        self.assertEqual(m.get(0, 1), 5)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(2, 3), 9)

    def test_serpentine(self):
        m = matrix.Matrix(list(range(12)), 3, serpentine_x=True)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(1, 0), 1)
        self.assertEqual(m.get(0, 1), 5)
        self.assertEqual(m.get(1, 1), 4)
        self.assertEqual(m.get(2, 2), 8)
        self.assertEqual(m.get(2, 3), 9)
