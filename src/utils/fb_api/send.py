import os
import json
import requests
import config
from src.utils.log import log
from templates.quick_replies import *


ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', config.ACCESS_TOKEN)
params = {
    "access_token": ACCESS_TOKEN
}
headers = {
    "Content-Type": "application/json"
}

payload = {
    'intent': '',
    'entities': {
        'tag': [
            {
                'value': ''
            }
        ]
    }
}

ANSWER_RATING_POINTS = {
    'Vulgar': -20,
    'Bad': -10,
    'Unrelated': -5,
    'Average': 1,
    'Good': 10,
    'Best': 20,
    'OOW': 100
}


def send_message(recipient_id, message_text):
    """
    Sends the messaged_text to recipient with given recipient_id

    :param recipient_id: unique facebook id of the user, to whom the message is to be sent.
    :param message_text: The message to be sent to the recipient.
    :return: None
    """
    if message_text == 'NULL' or message_text is None:
        return
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    if type(message_text) is dict:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": message_text
        })
    else:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def get_answer_feedback(asker_id, responder_id, question_id, question):
    """
    Post a quick reply for askers to rate the users for answers they got.

    :param asker_id: unique facebook id of the asker.
    :param responder_id: unique facebook id of the person qho answered asker's question.
    :param question_id: unique id of the question answered.
    :param question: question text corresponding to the question_id
    :return: None
    """
    log("sending feedback callback message to {recipient}".format(recipient=asker_id))
    quick_reply_buttons = dict()
    for rating_text, rating_point in ANSWER_RATING_POINTS.iteritems():
        quick_reply_buttons = add_quick_reply(quick_reply_buttons, rating_text,
                                              set_payload('rating', "{0}, {1}, {2}, {3}, {4}".format(
                                                  rating_point, rating_text, responder_id, question_id, question)
                                              ))

    data = json.dumps({
        "recipient": {
            "id": asker_id
        },
        "message": {
            "text": "Rate the answer: "
                    "(Marking OOW(Out of World), means you are satisfied, and don't want any more answers)",
            "quick_replies": quick_reply_buttons['quick_replies']
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def is_ascii(s):
    """
    Checks if the string (s) has any non-askii character.

    :param s: The string which is checked
    :return: True, is the string consists of all ascii characters, else returns False.
    """
    return all(ord(c) < 128 for c in s)


def set_payload(intent, tag):
    payload['intent'] = intent
    payload['entities']['tag'][0]['value'] = tag
    return payload
