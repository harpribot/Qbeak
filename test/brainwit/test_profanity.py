import unittest
from test.brainwit import *


class TestProfanity(unittest.TestCase):
    def test_profanity_1(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("Bakchod"))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_2(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("This is a stupid question"))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_3(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query(
            "Why are you asking this stupid question ?"))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_4(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("Shut up you fuckface."))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_5(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("You are an asshole."))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_6(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("Who is a chutiya?"))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_7(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("Kya chutiyaap hai ye."))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_8(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("Fuck off"))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_9(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query("Go to hell"))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_profanity_10(self):
        trait, confidence = get_trait_and_confidence(brainwit_handle.process_query(
            "Initially i thought that it was a reasonable question,"
            " but now that I have looked at it once, "
            "I have completely understood that this is a "
            "fuckin stupid question. Go to hell asshole."))
        self.assertEqual(trait, 'profanity')
        self.assertGreaterEqual(confidence, 0.8)

    def test_non_profanity_1(self):
        trait, _ = get_trait_and_confidence(brainwit_handle.process_query("Who is President of USA?"))
        self.assertNotEqual(trait, 'profanity')

    def test_non_profanity_2(self):
        trait, _ = get_trait_and_confidence(brainwit_handle.process_query("Who is Trump?"))
        self.assertNotEqual(trait, 'profanity')

    def test_non_profanity_3(self):
        trait, _ = get_trait_and_confidence(brainwit_handle.process_query("Is this profanity?"))
        self.assertNotEqual(trait, 'profanity')

    def test_non_profanity_4(self):
        trait, _ = get_trait_and_confidence(brainwit_handle.process_query("I am not using profane language"))
        self.assertNotEqual(trait, 'profanity')

    def test_non_profanity_5(self):
        trait, _ = get_trait_and_confidence(brainwit_handle.process_query("There is heaven and hell"))
        self.assertNotEqual(trait, 'profanity')






