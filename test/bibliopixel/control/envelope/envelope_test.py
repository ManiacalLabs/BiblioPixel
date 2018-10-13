import math, statistics, unittest
from fractions import Fraction
from bibliopixel.control.envelope import envelope
from test.bibliopixel.control.envelope.segments_test import function_tester


class EnvelopeTest(unittest.TestCase):
    def test_identity(self):
        env = envelope.Linear()
        expected = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0]
        function_tester(env, self, expected)

    def test_disable(self):
        env = envelope.Linear(base_value=0.5, enabled=False)
        expected = [0.5] * 11
        function_tester(env, self, expected)

    def test_offset_and_scale(self):
        env = envelope.Linear(offset=0.05, scale=2)
        expected = [0.05, 0.25, 0.45, 0.65, 0.85,
                    1.05, 1.25, 1.45, 1.65, 1.85, 0.05]
        function_tester(env, self, expected)

    def test_period(self):
        env = envelope.Linear(period=2)
        expected = [i / 20 for i in range(20)] + [0]
        function_tester(env, self, expected, 10)

    def test_symmetry(self):
        env = envelope.Linear(symmetry=Fraction(1) / 3)
        expected = [0 / 32, 6 / 32, 12 / 32, 17 / 32, 20 / 32,
                    23 / 32, 26 / 32, 29 / 32, 0 / 32]
        function_tester(env, self, expected)

    def test_sine(self):
        env = envelope.Sine()
        expected = [math.sin(i * math.pi / 5) for i in range(11)]
        function_tester(env, self, expected)

    def test_square(self):
        env = envelope.Square()
        expected = [0, 0, 0, 0, 1, 1, 1, 1, 0]
        function_tester(env, self, expected)

        env = envelope.Square(duty_cycle=Fraction(1, 6))
        expected = [0, 0, 0, 0, 0, 0, 0, 1, 0]
        function_tester(env, self, expected)

        env = envelope.Square(duty_cycle=Fraction(5, 6))
        expected = [0, 0, 1, 1, 1, 1, 1, 1, 0]
        function_tester(env, self, expected)

    def test_triangular(self):
        env = envelope.Triangular()
        expected = [0, 0.25, 0.5, 0.75]
        expected += [1] + expected[::-1]
        function_tester(env, self, expected)

    def _random(self, env, min_mean, max_mean, min_stdev, max_stdev,
                test_count=3, sample_count=300):
        mmin, smin, mmax, smax = 100, 100, 0, 0
        for i in range(test_count):
            values = [env(0) for i in range(sample_count)]
            mean, stdev = statistics.mean(values), statistics.stdev(values)
            mmax = max(mmax, mean)
            mmin = min(mmin, mean)
            smax = max(smax, stdev)
            smin = min(smin, stdev)

        self.assertGreater(mmin, min_mean)
        self.assertLess(mmax, max_mean)
        self.assertGreater(smin, min_stdev)
        self.assertLess(smax, max_stdev)

        return mmin, mmax, smin, smax

    def test_random(self):
        self._random(envelope.Random(), 0.35, 0.65, 0.20, 0.35)

    def test_gaussian(self):
        self._random(envelope.Gaussian(), 0.4, 0.6, 0.15, 0.35)
        self._random(envelope.Gaussian(stdev=0.1), 0.45, 0.55, 0.08, 0.12)
        self._random(envelope.Gaussian(mean=1.0), 0.9, 1.1, 0.20, 0.30)

    def test_empty_segments(self):
        env = envelope.Segments()

        expected = []
        function_tester(env, self, expected)

        expected = [0, 0, 0, 0]
        function_tester(env, self, expected)

    def test_simple_segments(self):
        env = envelope.Segments([1, 2, 3, 4])
        self.assertEqual(env.period, 1)

        expected = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 0]
        function_tester(env, self, expected)

    def test_simple_segments2(self):
        env = envelope.Segments([1, 1.5, 3, 7])
        self.assertEqual(env.period, 1)

        expected = [0, 0.5, 1, 1.25, 1.5, 2.25, 3, 5, 0]
        function_tester(env, self, expected)

    def test_decreasing_segments(self):
        env = envelope.Segments([1, 3, 2, 4])
        self.assertEqual(env.period, 1)

        expected = [0, 0.5, 1, 2, 3, 2.5, 2, 3, 0]
        function_tester(env, self, expected)
