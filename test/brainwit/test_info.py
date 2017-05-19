import unittest
from src.utils.handlers import Handler

handle = Handler()
brainwit_handle = handle.wit().brain()


class TestInfo(unittest.TestCase):
    def test_about(self):
        self.assertEqual(brainwit_handle.process_query("Who is Ubik?")[1], "about")
        self.assertEqual(brainwit_handle.process_query("What is Ubik?")[1], "about")
        self.assertEqual(brainwit_handle.process_query("Who are you?")[1], "about")
        self.assertEqual(brainwit_handle.process_query("What are you?")[1], "about")
        self.assertEqual(brainwit_handle.process_query("Who is Ubik")[1], "about")
        self.assertEqual(brainwit_handle.process_query("What is Ubik")[1], "about")
        self.assertEqual(brainwit_handle.process_query("Who are you")[1], "about")
        self.assertEqual(brainwit_handle.process_query("What do you do?")[1], "about")

    def test_not_about(self):
        self.assertNotEqual(brainwit_handle.process_query("Who is Barack Obama?")[1], "about")
        self.assertNotEqual(brainwit_handle.process_query("Who is Donald Trump?")[1], "about")
        self.assertNotEqual(brainwit_handle.process_query("What is Phenol?")[1], "about")
        self.assertNotEqual(brainwit_handle.process_query("What is NCAA?")[1], "about")

    def test_help(self):
        self.assertEqual(brainwit_handle.process_query("help me please")[1], "help")
        self.assertEqual(brainwit_handle.process_query("help")[1], "help")
        self.assertEqual(brainwit_handle.process_query("this is so confusing")[1], "help")
        self.assertEqual(brainwit_handle.process_query("i am confused")[1], "help")
        self.assertEqual(brainwit_handle.process_query("how to use Ubik?")[1], "help")
        self.assertEqual(brainwit_handle.process_query("how to use")[1], "help")

    def test_not_help(self):
        self.assertNotEqual(brainwit_handle.process_query("Help required. What is 2^20 ?")[1], "help")
        self.assertNotEqual(brainwit_handle.process_query("I need some help understanding string theory?")[1],
                            "help")
        self.assertNotEqual(brainwit_handle.process_query("Can anyone help me with boolean circuits?")[1], "help")
        self.assertNotEqual(brainwit_handle.process_query("I will be more than happy to help you. "
                                                             "So Boolean circuits is yet another "
                                                             "theoretical concept.")[1], "help")

    def test_statistics(self):
        self.assertEqual(brainwit_handle.process_query("ranking")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("my rank")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("my standing")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("what is my karma score?")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("karma score")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("my karma")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("karma points")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("statistics")[1], "ranking")
        self.assertEqual(brainwit_handle.process_query("my karma score please")[1], "ranking")

    def test_not_statistics(self):
        self.assertNotEqual(brainwit_handle.process_query("Help me")[1], "ranking")
        self.assertNotEqual(brainwit_handle.process_query("Define karma?")[1], "ranking")
        self.assertNotEqual(brainwit_handle.process_query("IPL statistics?")[1], "ranking")
        self.assertNotEqual(brainwit_handle.process_query("What is karma?")[1], "ranking")

    def test_greeting(self):
        self.assertEqual(brainwit_handle.process_query("hi")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("hello")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("hi ubik")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("hello ubik")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("hola")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("namaste")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("bonjour")[1], "greeting")
        self.assertEqual(brainwit_handle.process_query("salaam")[1], "greeting")

    def test_not_greeting(self):
        self.assertNotEqual(brainwit_handle.process_query("Hello! Thanks for the question. "
                                                             "I will try my best to answer it. So")[1], "greeting")
        self.assertNotEqual(brainwit_handle.process_query("hi ubik! Can you give me my ranking?")[1], "greeting")
        self.assertNotEqual(brainwit_handle.process_query("hello ubik. My score please")[1], "greeting")

    def test_joke(self):
        self.assertEqual(brainwit_handle.process_query("joke please")[1], "joke")
        self.assertEqual(brainwit_handle.process_query("I am getting bored")[1], "joke")
        self.assertEqual(brainwit_handle.process_query("humor me")[1], "joke")
        self.assertEqual(brainwit_handle.process_query("make me laugh")[1], "joke")

    def test_not_joke(self):
        self.assertNotEqual(brainwit_handle.process_query("this is not a joke")[1], "joke")
        self.assertNotEqual(brainwit_handle.process_query("we should have good humor")[1], "joke")
        self.assertNotEqual(brainwit_handle.process_query("humor takes you long way")[1], "joke")
        self.assertNotEqual(brainwit_handle.process_query("laughter is the best medicine")[1], "joke")
        self.assertNotEqual(brainwit_handle.process_query("she makes me laugh")[1], "joke")
