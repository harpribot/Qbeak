import unittest
from test.brainwit import *


class TestQuotes(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("inspirational quotes")), "quote")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("good quotes")), "quote")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("more quotes")), "quote")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("quotes")), "quote")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("quotation")), "quote")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("don't quote me")), "quote")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("quotes are bad")), "quote")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("i don't like quotes")), "quote")
