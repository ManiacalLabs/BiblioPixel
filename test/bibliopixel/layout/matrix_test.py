import contextlib, itertools, os, time, unittest
from . import matrix_results
from bibliopixel.drivers.driver_base import DriverBase
from bibliopixel.layout import Matrix
from bibliopixel.project import data_maker
from bibliopixel.util import log


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

    def line_at(self, y):
        return ''.join(self.text_at(x, y) for x in range(self.matrix.width))

    def to_strings(self):
        return tuple(self.line_at(y) for y in range(self.matrix.height))

    def name_of_test(self):
        name = self.id().split('.')[-1]
        if name.startswith('test_'):
            name = name[len('test_'):]
        return name.upper()

    def dump(self):
        # Dump the result to a file, if enabled.
        pass

    @contextlib.contextmanager
    def matrix_test(self, width=16, height=16):
        d = DriverBase(num=width * height)
        self.matrix = Matrix(d, width=width, height=height, maker=self.maker)

        yield  # Perform your operation here.

        self.dump()
        expected = getattr(matrix_results, self.name_of_test())
        actual = self.to_strings()
        if expected != actual:
            log.printer('Expected:', *(repr(s) for s in expected), sep='\n')
            log.printer('Actual:', *(repr(s) for s in actual), sep='\n')
            self.assertTrue(False)

    def test_empty(self):
        with self.matrix_test(4, 4):
            pass

    def test_horizontal_line(self):
        with self.matrix_test():
            self.matrix.drawLine(0, 0, 15, 0, WHITE)

    def test_vertical_line(self):
        with self.matrix_test():
            self.matrix.drawLine(0, 0, 0, 15, WHITE)

    def test_vertical_line2(self):
        with self.matrix_test():
            self.matrix.drawLine(1, 0, 1, 15, WHITE)

    def test_draw_circle1(self):
        with self.matrix_test():
            self.matrix.drawCircle(8, 8, 6, WHITE)

    def test_draw_circle2(self):
        with self.matrix_test(8, 8):
            self.matrix.drawCircle(4, 4, 15, WHITE)

    def test_draw_circle3(self):
        with self.matrix_test(4, 12):
            self.matrix.drawCircle(4, 6, 20, WHITE)

    def test_fill_circle1(self):
        with self.matrix_test():
            self.matrix.fillCircle(8, 8, 6, WHITE)

    def test_fill_circle2(self):
        with self.matrix_test(8, 8):
            self.matrix.fillCircle(4, 4, 15, WHITE)

    def test_fill_circle3(self):
        with self.matrix_test(4, 12):
            self.matrix.fillCircle(4, 6, 20, WHITE)

    def test_bresenham0(self):
        with self.matrix_test(8, 8):
            self.matrix.bresenham_line(0, 0, 8, 8, WHITE)

    def test_bresenham1(self):
        with self.matrix_test(8, 8):
            self.matrix.bresenham_line(8, 8, 0, 0, WHITE)

    def test_bresenham2(self):
        with self.matrix_test():
            self.matrix.bresenham_line(3, 5, 15, 18, WHITE)

    def test_bresenham3(self):
        with self.matrix_test():
            self.matrix.bresenham_line(15, 18, 3, 5, WHITE)

    def test_wu0(self):
        with self.matrix_test(8, 8):
            self.matrix.wu_line(0, 0, 8, 8, WHITE)

    def test_wu1(self):
        with self.matrix_test(8, 8):
            self.matrix.wu_line(8, 8, 0, 0, WHITE)

    def test_wu2(self):
        with self.matrix_test():
            self.matrix.wu_line(3, 5, 15, 18, WHITE)

    def test_wu3(self):
        with self.matrix_test():
            self.matrix.wu_line(15, 18, 3, 5, WHITE)

    def test_draw_rect(self):
        with self.matrix_test():
            self.matrix.drawRect(3, 5, 3, 2, WHITE)

    def test_fill_rect(self):
        with self.matrix_test():
            self.matrix.fillRect(3, 5, 6, 4, WHITE)

    def test_fill_screen(self):
        with self.matrix_test():
            self.matrix.fillScreen(WHITE)

    def DISABLED_test_draw_round_rect(self):
        with self.matrix_test():
            self.matrix.drawRoundRect(3, 5, 6, 7, 7, WHITE)

    def DISABLED_test_fill_round_rect(self):
        with self.matrix_test():
            self.matrix.fillRoundRect(3, 5, 6, 7, 7, WHITE)

    def test_draw_triangle(self):
        with self.matrix_test():
            self.matrix.drawTriangle(0, 0, 11, 4, 5, 12, WHITE)

    def DISABLED_test_fill_triangle(self):
        with self.matrix_test():
            self.matrix.fillTriangle(0, 0, 11, 4, 5, 12, WHITE)

    def test_draw_text(self):
        with self.matrix_test(32, 10):
            self.matrix.drawText('abc', color=WHITE)


class MatrixTest(BaseMatrixTest):
    maker = data_maker.Maker()


class SharedMatrixTest(BaseMatrixTest):
    maker = data_maker.Maker(shared_memory=True, floating=True)


class SharedMatrixIntegerTest(BaseMatrixTest):
    maker = data_maker.Maker(shared_memory=True, floating=False)


class FloatNumpyMatrixTest(BaseMatrixTest):
    maker = data_maker.Maker(numpy_dtype='float')


class Uint8NumpyMatrixTest(BaseMatrixTest):
    maker = data_maker.Maker(numpy_dtype='uint8')


class Int8NumpyMatrixTest(BaseMatrixTest):
    maker = data_maker.Maker(numpy_dtype='int8')


class DumpTest(BaseMatrixTest):
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


del BaseMatrixTest  # http://stackoverflow.com/a/22836015/43839
