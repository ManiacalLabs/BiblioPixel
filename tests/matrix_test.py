import pytest

from bibliopixel.led import LEDMatrix
from bibliopixel.drivers.driver_base import DriverBase

WHITE = (255, 255, 255)


def make_matrix(width, height, **kwds):
    driver = DriverBase(num=width * height)
    return LEDMatrix(driver, width=width, height=height, **kwds)


def assert_changed(matrix, expected):
    changed = [i for i, c in enumerate(matrix._colors) if c[0]]
    if changed != expected:
        print(changed)
    assert changed == expected


def assert_unchanged(matrix, expected):
    unchanged = [i for i, c in enumerate(matrix._colors) if not c[0]]
    assert unchanged == expected


def test_draw_circle1(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.drawCircle(8, 8, 6, WHITE)
        expected = [
            38, 39, 40, 41, 42, 52, 58, 68,
            76, 82, 92, 98, 110, 113, 125, 130,
            142, 145, 157, 162, 174, 178, 188,
            196, 204, 212, 218, 230, 231, 232, 233, 234]
        assert_changed(matrix, expected)
    benchmark(test)


def test_draw_circle2(benchmark):
    matrix = make_matrix(width=8, height=8)

    def test():
        matrix.drawCircle(4, 4, 15, WHITE)
        expected = [3, 13, 17, 31]  # Why isn't this empty!?
        assert_changed(matrix, expected)
    benchmark(test)


def test_draw_circle3(benchmark):
    matrix = make_matrix(width=4, height=12)

    def test():
        matrix.drawCircle(4, 6, 20, WHITE)
        expected = [0]
        assert_changed(matrix, expected)  # Huh?
    benchmark(test)


def test_fill_circle1(benchmark):
    matrix = make_matrix(width=16, height=16)
    def test():
        matrix.fillCircle(8, 8, 6, WHITE)
        expected = [
            38, 39, 40, 41, 42, 52, 53, 54, 55, 56, 57, 58, 68, 69, 70, 71,
            72, 73, 74, 75, 76, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92,
            98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 113,
            114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 130,
            131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 145,
            146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 162,
            163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 178,
            179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 196, 197, 198,
            199, 200, 201, 202, 203, 204, 212, 213, 214, 215, 216, 217, 218,
            230, 231, 232, 233, 234]
        assert_changed(matrix, expected)
    benchmark(test)


def test_fill_circle2(benchmark):
    matrix = make_matrix(width=8, height=8)

    def test():
        matrix.fillCircle(4, 4, 15, WHITE)
        expected = []
        assert_unchanged(matrix, expected)
    benchmark(test)


def test_fill_circle3(benchmark):
    matrix = make_matrix(width=4, height=12)

    def test():
        matrix.fillCircle(4, 6, 20, WHITE)
        expected = []
        assert_unchanged(matrix, expected)
    benchmark(test)


def test_bresenham1(benchmark):
    matrix = make_matrix(width=8, height=8)
    expected = [0, 14, 18, 28, 36, 42, 54, 56]

    def test():
        matrix.bresenham_line(0, 0, 8, 8, WHITE)
        assert_changed(matrix, expected)
        matrix.bresenham_line(8, 8, 0, 0, WHITE)
        assert_changed(matrix, expected)

    benchmark(test)


def test_bresenham2(benchmark):
    matrix = make_matrix(width=16, height=16)
    expected = [92, 100, 122, 134, 152, 168, 182, 201, 213, 235, 243]

    def test():
        matrix.bresenham_line(3, 5, 15, 18, WHITE)
        assert_changed(matrix, expected)

        matrix.bresenham_line(15, 18, 3, 5, WHITE)
        assert_changed(matrix, expected)
    benchmark(test)


def test_wu1(benchmark):
    matrix = make_matrix(width=8, height=8)
    expected = [0, 14, 18, 28, 36, 42, 54, 56]

    def test():
        matrix.wu_line(0, 0, 8, 8, WHITE)
        assert_changed(matrix, expected)

        matrix.wu_line(8, 8, 0, 0, WHITE)
        assert_changed(matrix, expected)

    benchmark(test)


def test_wu2(benchmark):
    matrix = make_matrix(width=16, height=16)
    expected = [92, 99, 100, 122, 123, 133, 134, 152, 153,
                167, 168, 182, 183, 201, 202, 212, 213, 235, 236,
                242, 243]

    def test():
        matrix.wu_line(3, 5, 15, 18, WHITE)
        assert_changed(matrix, expected)

        matrix.wu_line(15, 18, 3, 5, WHITE)
        assert_changed(matrix, expected)
    benchmark(test)


def test_draw_rect(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.drawRect(3, 5, 3, 2, WHITE)
        expected = [90, 91, 92, 99, 100, 101]
        assert_changed(matrix, expected)
    benchmark(test)


def test_fill_rect(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.fillRect(3, 5, 6, 4, WHITE)
        expected = [87, 88, 89, 90, 91, 92, 99, 100, 101, 102, 103, 104, 119,
                    120, 121, 122, 123, 124, 131, 132, 133, 134, 135, 136]
        assert_changed(matrix, expected)
    benchmark(test)


def test_fill_screen(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.fillScreen(WHITE)
        expected = []
        assert_unchanged(matrix, expected)
    benchmark(test)


def DISABLED_test_draw_round_rect(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.drawRoundRect(3, 5, 6, 7, 7, WHITE)
        expected = []
        assert_changed(matrix, expected)
    benchmark(test)


def DISABLED_test_fill_round_rect(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.fillRoundRect(3, 5, 6, 7, 7, WHITE)
        expected = []
        assert_changed(matrix, expected)
    benchmark(test)


def test_draw_triangle(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.drawTriangle(0, 0, 11, 4, 5, 12, WHITE)
        expected = [0, 1, 27, 28, 29, 31, 33, 37, 38, 54, 55, 56, 62, 66, 74,
                    75, 85, 93, 98, 106, 118, 124, 131, 136, 152, 155, 164, 167,
                    185, 186, 197]
        assert_changed(matrix, expected)
    benchmark(test)


def DISABLED_test_fill_triangle(benchmark):
    matrix = make_matrix(width=16, height=16)

    def test():
        matrix.fillTriangle(0, 0, 11, 4, 5, 12, WHITE)
        expected = []
        assert_changed(matrix, expected)
    benchmark(test)


def test_draw_text(benchmark):
    matrix = make_matrix(width=32, height=10)

    def test():
        matrix.drawText('abc', color=WHITE)
        expected = [6, 57, 65, 66, 70, 72, 73, 77, 78, 79, 111, 115, 117, 120,
                    121, 124, 129, 130, 131, 134, 138, 140, 175, 179, 181, 184,
                    185, 188, 191, 193, 194, 195, 196, 198, 200, 201, 205, 206,
                    207]
        assert_changed(matrix, expected)
    benchmark(test)
