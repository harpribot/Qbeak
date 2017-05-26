import unittest
from test.brainwit import *


class TestRanking(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("ranking")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("my rank")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("my standing")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("what is my karma score?")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("karma score")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("my karma")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("karma points")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("statistics")), "ranking")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("my karma score please")), "ranking")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Help me")), "ranking")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Define karma?")), "ranking")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("IPL statistics?")), "ranking")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("What is karma?")), "ranking")
