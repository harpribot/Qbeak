import unittest
from test.brainwit import *


class TestFacts(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("some interesting facts")), "fact")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("fact of the day")), "fact")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("cool facts")), "fact")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("more facts")), "fact")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("This is a fact.")), "fact")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("As a matter of fact")), "fact")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("factorial")), "fact")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("fact checking is important")), "fact")
