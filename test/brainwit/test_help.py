import unittest
from test.brainwit import *


class TestHelp(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("help me please")), "help")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("help")), "help")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("this is so confusing")), "help")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("i am confused")), "help")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("how to use Ubik?")), "help")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("how to use")), "help")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Help required. What is 2^20 ?")), "help")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query(
            "I need some help understanding string theory?")), "help")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query(
            "Can anyone help me with boolean circuits?")), "help")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query(
            "I will be more than happy to help you. So Boolean circuits is yet another theoretical concept.")), "help")
