import json
import random
import wikipedia
from templates.generic import *
from templates.text import TextTemplate
import config

JOKES_DATA = open(config.JOKES_SOURCE_FILE).read()
JOKES = json.loads(JOKES_DATA)['jokes']
GREETING_DATA = open(config.GREETING_SOURCE_FILE).read()
GREETING = json.loads(GREETING_DATA)['greeting']
GOODBYE_DATA = open(config.GREETING_SOURCE_FILE).read()
GOODBYE = json.loads(GOODBYE_DATA)['bye']
MOTIVATION_DATA = open(config.MOTIVATIONS_SOURCE_FILE).read()
MOTIVATION = json.loads(MOTIVATION_DATA)['motivations']
PUZZLE_DATA = open(config.PUZZLES_SOURCE_FILE).read()
PUZZLE = json.loads(PUZZLE_DATA)['puzzles']
QUOTES_JSON = open(config.QUOTES_SOURCE_FILE).read()
QUOTES = json.loads(QUOTES_JSON)['quotes']
FACTS_JSON = open(config.FACTS_SOURCE_FILE).read()
FACTS = json.loads(FACTS_JSON)['facts']

MAX_PROFANITY = 5
ADMIN_EMAIL = 'harshalpriyadarshi6@gmail.com'


def profanity_feedback():
    return "Sorry we can't send your message as it contains a lot of profanity."


def moderation_submission_feedback():
    return "Your response has been submitted for moderation. Once approved you will be notified."


def about_response():
    return "Hi! I am Qbeak.\n\nI am your personal Q&A (Question and Answer) bot." \
           "I will get the best people to answer your questions." \
           "Ask anything sensible. But please [PLEASE] don't include any personal details," \
           "as they will be delivered as it is to all users getting an A2A.\n" \
           "This is an anonymous Q&A platform, built on confidence." \
           "If you ask indecent questions or give inappropriate answers you will get substantial hit" \
           "to your karma score and may lose your access to my service. We get feedback on your questions and" \
           "answers and closely monitor them.\n"


def question_answer_help_response():
    return "1. To ask a question\n<Question Text> ?\n\n" \
           "Example:\nWho is Ubik?\n\n" \
           "NOTE: Your question should end with question mark(?)\n" \
           "------------------------------\n\n" \
           "2. To give an answer to a question\n[<question id (qid)>] <Answer Text>\n\n" \
           "Example:\n[108] Ubik is a Zombie who is getting younger by getting you answers" \
           "to your questions\n\nType 'done' to complete answering, or 'cancel' to cancel he present response\n\n" \
           "NOTE: The above example is an answer to a question with qid=108\n" \
           "------------------------------\n"


def sample_examples_response():
    return "Some Example:\n* Hello Qbeak\n" \
           "* Who are you ?\n" \
           "* Help me please\n" \
           "* my karma score\n" \
           "* pause subscription\n" \
           "* restart subscription\n " \
           "* Who is Barack Obama ?\n" \
           "* Who is Elvis Presley ?\n" \
           "* add tags\n" \
           "* remove tags\n" \
           "* joke please\n" \
           "* i am getting bored\n" \
           "* Bye Qbeak"


def confusion_response():
    return "Sorry, I don't understand what you meant. " \
           "Type 'help' for general help and 'QA' to know how to ask and respond to questions."


def help_response():
    return "Hi, I am Qbeak. You can ask me your question. Here are some ways to interact.\n" \
           "* Type 'about Qbeak' for knowing about me.\n" \
           "* Type 'QA' to know how to ask and answer questions.\n" \
           "* Type 'ranking' for knowing your karma score.\n" \
           "* Type 'pause' to pause subscription(Lose 10 karma pts/day).\n" \
           "* Type 'restart' to restart subscription.\n" \
           "* Type 'examples' to try some quick sample questions.\n" \
           "* Type 'profile' to see your Ubik profile.\n" \
           "* Type 'add tags' to add new tags to your skillset.\n" \
           "* Type 'remove tags' to remove tags from your skillset."


def joke_response():
    return random.choice(JOKES)


def bye_response():
    return random.choice(GOODBYE)


def facts_response():
    return random.choice(FACTS)


def greeting_response():
    return random.choice(GREETING)


def motivations_response():
    return random.choice(MOTIVATION)


def puzzles_response():
    return random.choice(PUZZLE)


def quotes_response():
    return random.choice(QUOTES)


def wiki_response(search_query):
    try:
        data = wikipedia.page(search_query)
        text_template = TextTemplate('Wikipedia summary of ' + data.title + ':\n' + data.summary)
        text = text_template.get_message()['text']
        button_template = ButtonTemplate(text)
        button_template.add_web_url('Wikipedia Link', data.url)
        response_message = button_template.get_message()
    except wikipedia.exceptions.DisambiguationError, e:
        generic_template = GenericTemplate()
        image_url = 'https://en.wikipedia.org/static/images/project-logos/enwiki-2x.png'
        pageids = set()
        for option in e.options:
            try:
                data = wikipedia.page(option)
                if data.pageid in pageids:
                    continue
                pageids.add(data.pageid)
                buttons = ButtonTemplate()
                buttons.add_web_url('Wikipedia Link', data.url)
                '''@TODO: Figure Postbacks
                payload = {
                    'intent': 'wiki',
                    'entities': {
                        'tag': [
                            {
                                'value': option
                            }
                        ]
                    }
                }
                buttons.add_postback('Wikipedia Summary', json.dumps(payload))
                '''
                generic_template.add_element(title=data.title, item_url=data.url,
                                             image_url=image_url, buttons=buttons.get_buttons())
            except Exception, ex:
                pass
        response_message = generic_template.get_message()

    return response_message


def question_save_feedback(question_stored):
    """
    Sends a immediate feedback, explaining, if the question was saved or not.

    :return: Feedback message
    """
    if question_stored:
        response = "Your question has been saved. " \
                   "I will get back to you with an expert's answer. " \
                   "Keep your fingers crossed. " \
                   "Meanwhile, you can ask another question, or post answer for requested question."
    else:
        response = "Sorry, there has been some issue with our server. We are working hard to fix it up. " \
                   "Try again after sometime."

    return response


def answer_save_feedback(answer_stored):
    """
    Sends a immediate feedback, explaining, if the answer was saved or not.

    :param answer_stored: True, if the answer was stored else False
    :return: Feedback text.
    """
    if answer_stored:
        response = "Thanks for your answer. Your answer has been saved. " \
                   "I will get back to you when the destined asker, rates your response. " \
                   "Keep your fingers crossed. Hopefully the asker will give you good ratings, " \
                   "and your karma points will boost up." \
                   "Meanwhile, you can ask another question, or post answer for requested question."
    else:
        response = "Sorry, you did not enter the Answer in the required format. " \
                   "Eg - \"[<placeholder for qid>] <Placeholder for Answer>\". Try again"

    return response


def response_not_requested_feedback(question_id):
    """
    Feedback when the user tries to answer a question, he was not sent.
    :return: Feedback message
    """
    return "You were not asked any question corresponding to this question ID -> {0}." \
           "\n We are sorry, you can't answer it.".format(question_id)


def finish_present_answer_feedback(question_id):
    """
    Feedback when the user tries to answer another question, when he is in mid of answering a question.

    :param question_id: Q-id of the question, you are currently answering
    :return: Feedback text
    """
    return "Please complete answering present question: QID ->{0}".format(question_id)


def answer_cancelled_feedback(question_id):
    return 'Your response to the question (QID: {0}) is cancelled.'.format(question_id)


def asker_feedback_response(is_karma_updated):
    """
    fetches response to the feedback posted by the asker. Depends on the fact, that the karma was updated or not.

    :param is_karma_updated: True, if the karma was updated, else False
    :return: The feedback sent to the question answerer.
    """
    if is_karma_updated:
        response = "Thanks for your feedback. Your feedback has been saved, "\
               "and the person who answered will be notified."
    else:
        response = "Dang, our servers crashed. Lol. Finally something more than"\
               " my brain can explode. Delicious tiny brain."

    return response


def subscription_update_request_feedback(flag):
    """
    The subscription message sent to the person requesting pausing or restarting the subscription.

    :param flag: True, means subscription should be made active, False, means subscription should be made inactive.
    None, means there was some error.
    :return: subscription message
    """
    if flag is None:
        subscription_message = \
            "We were unable to update your subscription. We are working to fix this up. Sorry, says the Zombie."
    elif flag:
        subscription_message = \
            "Welcome back! Your subscription has been restarted. Best of luck answering questions."
    else:
        subscription_message = \
            "Your subscription has been paused. \n" \
            "For each day your subscription is inactive, you lose 10 karma points"

    return subscription_message


def barred_from_platform_response():
    return "You used profane words {0} times. Hence you have been barred. " \
           "Drop an email to administrator - {1}, with a request to unbar yourself.".format(
            MAX_PROFANITY, ADMIN_EMAIL)


def profanity_warning_response(profanity_count):
    return "Our moderator or system has found that you used profanity." \
           " You have only {0} profanity messages remaining before being barred.".format(
            MAX_PROFANITY - profanity_count)


def user_stat_request_feedback(percentile_standing, karma=None):
    """
    Sends the statistics message to the user about his karma

    :param karma: The karma rating of the user.
    :param percentile_standing: The percentile standing of the user.
    :return:
    """
    if percentile_standing is None:
        stats_message = "Sorry, we don't have ranking for you. Ask a question first."
    elif percentile_standing == -1:
        stats_message = "You need to ask at least one question, to be rated."
    else:
        stats_message = "Your karma score is:{0}\nYour karma score is above {1} percent of other users". \
            format(karma, percentile_standing)

    return stats_message


def useless_message_response(data):
    """
    Feedback sent to the asker/answerer if there message is found to be useless by the moderator.
    :param data:
    :return: feedback
    """
    return "Sorry, the moderator suggested that your message is not useful." + "\nFor:{0}".format(data)


def answer_feedback_to_answerer(rating, question, karma):
    "Hey dude, someone rated you ({0}), for Question: {1}. Your current karma point is: {2}". \
        format(rating, question, karma)
