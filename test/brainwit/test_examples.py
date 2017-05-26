import unittest
from test.brainwit import *


class TestExamples(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("some examples")), "examples")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("examples please")), "examples")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("examples")), "examples")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("How to use")), "examples")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Give example of Famous Author")),"examples")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("You have set an example")), "examples")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("examples make you learn quick")),"examples")
