import unittest
from test.brainwit import *


class TestPuzzles(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("i want some puzzles")), "puzzle")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("more puzzles")), "puzzle")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("puzzles")), "puzzle")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("Puzzles please")), "puzzle")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("This is puzzling")), "puzzle")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Puzzled me")), "puzzle")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Puzz")), "puzzle")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("I don't want puzzles")), "puzzle")
