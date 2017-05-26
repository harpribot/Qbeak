import unittest
from test.brainwit import *


class TestJokes(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("joke please")), "joke")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("I am getting bored")), "joke")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("humor me")), "joke")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("make me laugh")), "joke")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("this is not a joke")), "joke")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("we should have good humor")), "joke")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("humor takes you long way")), "joke")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("laughter is the best medicine")), "joke")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("she makes me laugh")), "joke")
