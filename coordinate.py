# -*- coding: utf-8 -*-
class Coordinate(object):
    def __init__(self, x, y):
        self._x, self._y = x, y

    def xy(self):
        return self._x, self._y

    def __eq__(self, other):
        return self.xy() == other.xy()

    def __add__(self, other):
        x, y = [v + ov for v, ov in zip(self.xy(), other.xy())]
        return Coordinate(x, y)

    def __sub__(self, other):
        x, y = [v - ov for v, ov in zip(self.xy(), other.xy())]
        return Coordinate(x, y)

    def __mul__(self, other):
        x, y = [v * ov for v, ov in zip(self.xy(), other.xy())]
        return Coordinate(x, y)

    def __hash__(self):
        return hash((self._x, self._y))

    def copy(self):
        return Coordinate(self._x, self._y)

if __name__ == '__main__':
    import unittest

    class Test(unittest.TestCase):
        def setUp(self):
            self.pos = Coordinate(1, 2)

        def testXY(self):
            self.assertEqual(self.pos.xy(), (1, 2))

        def testEqual(self):
            self.assertEqual(self.pos, Coordinate(1, 2))

        def testAdd(self):
            self.assertEqual(self.pos + Coordinate(2, 3), Coordinate(3, 5))

        def testMinus(self):
            self.assertEqual(Coordinate(4, 6) - self.pos, Coordinate(3, 4))

        def testMul(self):
            self.assertEqual(self.pos * Coordinate(2, 3), Coordinate(2, 6))

        def testHash(self):
            key = 'the key'
            d = {self.pos:key}
            self.assertEqual(d[Coordinate(1, 2)], key)

        def testCopy(self):
            copy = self.pos.copy()
            self.assertEqual(self.pos.xy(), copy.xy())

    unittest.main()
