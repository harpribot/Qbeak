import unittest
from test.brainwit import *


class TestAbout(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("Who is Qbeak?")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("What is Qbeak?")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("Who are you?")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("What are you?")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("Who is Qbeak")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("What is Qbeak")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("Who are you")), "about")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("What do you do?")), "about")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Who is Barack Obama?")), "about")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Who is Donald Trump?")), "about")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("What is Phenol?")), "about")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("What is NCAA?")), "about")
