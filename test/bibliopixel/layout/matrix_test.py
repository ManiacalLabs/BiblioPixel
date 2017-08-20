import os, itertools, time, unittest

from bibliopixel.project import data_maker
from bibliopixel.layout import Matrix
from bibliopixel.drivers.driver_base import DriverBase
from . import matrix_results


WHITE = (255, 255, 255)

DUMP_FILENAME = os.environ.get('BP_MATRIX_DUMP')

if DUMP_FILENAME:
    with open(DUMP_FILENAME, 'w') as fp:
        fp.write('# This was file was automatically generated on ')
        fp.write(time.strftime('%X %x %Z'))
        fp.write('\n')


class BaseMatrixTest(unittest.TestCase):

    def text_at(self, x, y):
        """Return text for a given pixel"""
        return '*' if any(self.matrix.get(x, y)) else ' '

    def to_strings(self):
        xrange = range(self.matrix.width)
        for y in range(self.matrix.height):
            yield ''.join(self.text_at(x, y) for x in xrange)

    def name_of_test(self):
        id = self.id().split('.')[-1]
        if id.startswith('test_'):
            id = id[len('test_'):]
        return id.upper()

    def make_matrix(self, width, height, **kwds):
        driver = DriverBase(num=width * height)
        self.matrix = Matrix(
            driver, width=width, height=height, maker=self.maker, **kwds)

    def dump(self):
        # Dump the result to a file, if enabled.
        pass

    def assert_in_results(self):
        result = getattr(matrix_results, self.name_of_test())
        self.assertEqual(tuple(self.to_strings()), result)

    def test_horizontal_line(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawLine(0, 0, 15, 0, WHITE)
        self.assert_in_results()

    def test_vertical_line(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawLine(0, 0, 0, 15, WHITE)
        self.assert_in_results()

    def test_vertical_line2(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawLine(1, 0, 1, 15, WHITE)
        self.assert_in_results()

    def test_draw_circle1(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawCircle(8, 8, 6, WHITE)
        self.assert_in_results()

    def test_draw_circle2(self):
        self.make_matrix(width=8, height=8)
        self.matrix.drawCircle(4, 4, 15, WHITE)
        self.assert_in_results()

    def test_draw_circle3(self):
        self.make_matrix(width=4, height=12)
        self.matrix.drawCircle(4, 6, 20, WHITE)
        self.assert_in_results()

    def test_fill_circle1(self):
        self.make_matrix(width=16, height=16)
        self.matrix.fillCircle(8, 8, 6, WHITE)
        self.assert_in_results()

    def test_fill_circle2(self):
        self.make_matrix(width=8, height=8)
        self.matrix.fillCircle(4, 4, 15, WHITE)
        self.assert_in_results()

    def test_fill_circle3(self):
        self.make_matrix(width=4, height=12)
        self.matrix.fillCircle(4, 6, 20, WHITE)
        self.assert_in_results()

    def test_bresenham0(self):
        self.make_matrix(width=8, height=8)
        self.matrix.bresenham_line(0, 0, 8, 8, WHITE)
        self.assert_in_results()

    def test_bresenham1(self):
        self.make_matrix(width=8, height=8)
        self.matrix.bresenham_line(8, 8, 0, 0, WHITE)
        self.assert_in_results()

    def test_bresenham2(self):
        self.make_matrix(width=16, height=16)
        self.matrix.bresenham_line(3, 5, 15, 18, WHITE)
        self.assert_in_results()

    def test_bresenham3(self):
        self.make_matrix(width=16, height=16)
        self.matrix.bresenham_line(15, 18, 3, 5, WHITE)
        self.assert_in_results()

    def test_wu0(self):
        self.make_matrix(width=8, height=8)
        self.matrix.wu_line(0, 0, 8, 8, WHITE)
        self.assert_in_results()

    def test_wu1(self):
        self.make_matrix(width=8, height=8)
        self.matrix.wu_line(8, 8, 0, 0, WHITE)
        self.assert_in_results()

    def test_wu2(self):
        self.make_matrix(width=16, height=16)
        self.matrix.wu_line(3, 5, 15, 18, WHITE)
        self.assert_in_results()

    def test_wu3(self):
        self.make_matrix(width=16, height=16)
        self.matrix.wu_line(15, 18, 3, 5, WHITE)
        self.assert_in_results()

    def test_draw_rect(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawRect(3, 5, 3, 2, WHITE)
        self.assert_in_results()

    def test_fill_rect(self):
        self.make_matrix(width=16, height=16)
        self.matrix.fillRect(3, 5, 6, 4, WHITE)
        self.assert_in_results()

    def test_fill_screen(self):
        self.make_matrix(width=16, height=16)
        self.matrix.fillScreen(WHITE)
        self.assert_in_results()

    def DISABLED_test_draw_round_rect(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawRoundRect(3, 5, 6, 7, 7, WHITE)
        self.assert_in_results()

    def DISABLED_test_fill_round_rect(self):
        self.make_matrix(width=16, height=16)
        self.matrix.fillRoundRect(3, 5, 6, 7, 7, WHITE)
        self.assert_in_results()

    def test_draw_triangle(self):
        self.make_matrix(width=16, height=16)
        self.matrix.drawTriangle(0, 0, 11, 4, 5, 12, WHITE)
        self.assert_in_results()

    def DISABLED_test_fill_triangle(self):
        self.make_matrix(width=16, height=16)
        self.matrix.fillTriangle(0, 0, 11, 4, 5, 12, WHITE)
        self.assert_in_results()

    def test_draw_text(self):
        self.make_matrix(width=32, height=10)
        self.matrix.drawText('abc', color=WHITE)
        self.assert_in_results()


class MatrixTest(BaseMatrixTest):
    maker = data_maker.Maker()
    indent = ''

    def dump(self):
        if not DUMP_FILENAME:
            return

        with open(DUMP_FILENAME, 'a') as fp:
            def writeln(*parts):
                if parts:
                    fp.write(self.indent)
                    fp.writelines(itertools.chain(*parts))
                fp.write('\n')

            writeln()
            writeln(self.name_of_test(), ' = (')

            for row in self.to_strings():
                writeln("    '", row, "',")

            writeln(')')


class SharedMatrixTest(BaseMatrixTest):
    maker = data_maker.Maker(shared_memory=True, floating=True)


class SharedMatrixIntegerTest(BaseMatrixTest):
    maker = data_maker.Maker(shared_memory=True, floating=False)


del BaseMatrixTest  # http://stackoverflow.com/a/22836015/43839
