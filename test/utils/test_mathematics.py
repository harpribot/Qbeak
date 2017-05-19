import unittest
from src.utils.stats import percentile


class TestMathematics(unittest.TestCase):
    def test_mathematics_zero_percentile(self):
        self.assertEqual(percentile(1, [1, 3]), 0.0)

    def test_mathematics_hundred_percentile(self):
        self.assertEqual(percentile(2, [1, 2]), 100.0)
