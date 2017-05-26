import unittest
from test.brainwit import *


class TestGoodbye(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("goodnight")), "goodbye")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("i have to go now")), "goodbye")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("gtg")), "goodbye")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("See you then.")), "goodbye")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Good")), "goodbye")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("What is meaning of Goodbye")), "goodbye")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("When to say Good night")), "goodbye")
