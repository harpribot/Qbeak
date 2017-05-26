import unittest
from test.brainwit import *


class TestGreeting(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(trait_if_present(brainwit_handle.process_query("hi")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("hello")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("hi ubik")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("hello ubik")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("hola")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("namaste")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("bonjour")), "greeting")
        self.assertEqual(trait_if_present(brainwit_handle.process_query("salaam")), "greeting")

    def test_negative(self):
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("Hello! Thanks for the question. "
                            "I will try my best to answer it. So")), "greeting")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("hi qbeak! Can you give me my ranking?")),
                            "greeting")
        self.assertNotEqual(trait_if_present(brainwit_handle.process_query("hello qbeak. My score please")), "greeting")
