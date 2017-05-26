import unittest
from test.brainwit import *


class TestProfile(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("my profile")), "profile")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("show my profile")), "profile")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("profile please")), "profile")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("Profile")), "profile")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Profiling")), "profile")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Pro file")), "profile")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("What is your profile")), "profile")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Racial Profiling")), "profile")
