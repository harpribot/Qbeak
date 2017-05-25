"""
MIT License

Copyright (c) 2017 Harshal Priyadarshi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from src.database.database import Database
from src.database.question import Question
from src.database.answer import Answer
from src.database.user import User
from src.event.databaseEvent import DatabaseEvent
from src.event.postbackEvent import PostbackEvent
from src.openraas.brainwit import BrainWit
from src.utils.fb_api.send import send_message
from src.utils.log import log


class Handler:
    def __init__(self):
        self.db_handle = self.DbHandler()
        self.event_handle = self.EvenHandler(self.db_handle)
        self.wit_handle = self.WitHandler(self.db_handle, self.event_handle)

    def database(self):
        return self.db_handle

    def event(self):
        return self.event_handle

    def wit(self):
        return self.wit_handle

    class DbHandler:
        def __init__(self):
            self.db = Database()
            self.question_handler = Question(self.db)
            self.answer_handler = Answer(self.db)
            self.user_handler = User(self.db)

        def user(self):
            return self.user_handler

        def question(self):
            return self.question_handler

        def answer(self):
            return self.answer_handler

        def database(self):
            return self.db

    class EvenHandler:
        def __init__(self, db_handle):
            self.database_event_handler = DatabaseEvent(db_handle)
            self.postback_event_handler = PostbackEvent(db_handle)

        def database(self):
            return self.database_event_handler

        def postback(self):
            return self.postback_event_handler

    class WitHandler:
        def __init__(self, db_handle, event_handle):
            self.brainwit_handler = BrainWit(db_handle, event_handle)

        def brain(self):
            return self.brainwit_handler


handle = Handler()


def handle_message(payload, sender_id, message_type="non-feedback"):
    """
    Handles payload, and redirect them to proper handler.

    :param payload: Message (or Quick Reply) payload
    :param sender_id: The unique facebook user id of the person who sent the payload
    :param message_type: The type of the GET request. "non-feedback" -> feedback not required from other user,
                                              "feedback" -> feedback required from other user.
    :return: None
    """
    status = handle.database().user().add_user_if_new(sender_id)  # always add the user to the database, if new.
    # status is not OK when the user is barred.
    if status != "OK":
        send_message(sender_id, status)
        return
    if message_type == "non-feedback":
        if payload.startswith('['):
            response_text = handle.database().answer().add_answer(payload, sender_id)
        elif payload.lower() == "done":
            cur = handle.database().db.get_cursor()
            cur.execute("SELECT answering_buffer FROM users WHERE user_id=%s", (sender_id,))
            answer = cur.fetchone()[0]
            if answer == '':
                return
            response_text = handle.event().database().check_for_moderation(answer, sender_id, handle)
            if response_text == "OK":
                response_text = handle.database().answer().add_answer(payload, sender_id)
        elif handle.database().user().get_current_answering_question(sender_id) is not None:
            response_text = handle.database().answer().add_answer(payload, sender_id)
        else:
            response_text = handle.wit().brain().get_response(sender_id, payload)
    elif message_type == "feedback":
        response_text = handle.event().postback().handle_postback(payload, sender_id)
    else:
        response_text = ""
        log("invalid message type sent to handler")

    send_message(sender_id, response_text)
