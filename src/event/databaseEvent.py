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
import json
import re
import random
from src.utils.fb_api.send import send_message, get_answer_feedback
from src.utils.log import log
from templates.generic import *


MODERATION_PAYLOAD = {
    'intent': 'moderation',
    'entities': {
        'tag': [
            {
                'value': ''
            }
        ]
    }
}

MODERATION_TYPES = ["YES", "NO", "PROFANE"]


class DatabaseEvent:

    def __init__(self, db_handle):
        """
        Event handler for handling event tiggers like Question being asked, Answer being given, feedback being posted.

        :param db_handle: object for Postgres database.
        """
        self.cur = db_handle.database().get_cursor()
        self.question_handler = db_handle.question()
        self.answer_handler = db_handle.answer()
        self.user_handler = db_handle.user()

    def new_question(self, question_id, question, asker_id):
        """
        Triggered when a new question is asked.
        Response: If number of users = 1, do nothing
                                     = 2, send question to the non-asker
                                     = 2+, send question to (n)/2 non-askers, where n = # non askers

        :param question_id: The unique id of the question that was posted.
        :param question: The question asked,
        :param asker_id: The unique facebook id of the person asking the question.
        :return: None
        """
        try:
            self.cur.execute("SELECT user_id FROM users WHERE user_id <> %s AND subscription=TRUE;", (asker_id,))
            non_askers = [x[0] for x in self.cur.fetchall()]
            if not non_askers:
                return
            request_message = "Can you answer this question? coz I can't as I don't have brains "
            question_message = "[Question][qid:{0}] {1}".format(question_id, question)
            if len(non_askers) == 1:
                send_message(int(non_askers[0]), request_message)
                send_message(int(non_askers[0]), question_message)
                self.cur.execute("UPDATE users SET sent_questions = array_append(sent_questions, %s)"
                                 " WHERE user_id=%s AND NOT sent_questions @> ARRAY[%s];",
                                 (question_id, non_askers[0], question_id))
            else:
                chosen_non_askers = random.sample(non_askers, min(4, (len(non_askers)) / 2))
                for recipient in chosen_non_askers:
                    send_message(int(recipient), request_message)
                    send_message(int(recipient), question_message)
                    self.cur.execute("UPDATE users SET sent_questions = array_append(sent_questions, %s)"
                                     " WHERE user_id=%s AND NOT sent_questions @> ARRAY[%s];",
                                     (question_id, recipient, question_id))
        except Exception, ex:
            log("Failed to fetch all non askers. Exception: {0}".format(ex))

    def new_answer(self, question_id, answer, sender_id):
        """
        Triggered when a new answer is given.
        Response: If has_answer = True, do nothing (as user is satisfied)
                                else, send asker the answer, and ask if he is satisfied.

        :param question_id: The unique id of the question that was answered.
        :param answer: Answer Text
        :param sender_id: The user id of the person who answered the question.
        :return: None
        """
        try:
            self.cur.execute("SELECT asker_id, question, has_answer FROM question WHERE question_id=%s;",
                             (question_id,))
            asker_id, question, has_answer = self.cur.fetchone()
            self.cur.execute("UPDATE users SET answered_questions = array_append(answered_questions, %s)"
                             " WHERE user_id=%s AND NOT answered_questions @> ARRAY[%s::INT];",
                             (question_id, sender_id, question_id))
            self.cur.execute("UPDATE users SET answering_questions = array_remove(answering_questions, %s)"
                             " WHERE user_id=%s;",
                             (question_id, sender_id))

            if has_answer:
                return
            if asker_id == sender_id:
                return

            try:
                respond_message = "Here is the answer to your question\nQuestion:{0}".format(question)
                answer_message = "Answer:\n {0}".format(answer)
                send_message(int(asker_id), respond_message)
                send_message(int(asker_id), answer_message)
                get_answer_feedback(int(asker_id), int(sender_id), question_id, question)
            except Exception, ex:
                log("Failed sending answer to asker. Exception:{0}".format(ex))
        except Exception, ex:
            log("Failed to fetch the answered question from the database. Exception:{0}".format(ex))

    def ask_answer(self, threads):
        """
        Triggered periodically, asking for an answer.

        :return:
        """
        pass

    def pause_subscription(self, user_id):
        """
        Pauses subscription, and sends feedback

        :param user_id: User id of the user whose subscription is to be paused.
        :return: Feedback of the pause subscription request.
        """
        return self.user_handler.update_subscription(user_id, False)

    def restart_subscription(self, user_id):
        """
        Restarts subscription, and sends feedback

        :param: user_id: User id of the user whose subscription is to be restarted.
        :return: Feedback of the restore subscription request.
        """
        return self.user_handler.update_subscription(user_id, True)

    def moderate(self, user_id, question, answer=None):
        """

        :param question:
        :param answer:
        :return:
        """
        if answer:
            question_answer = "Question:{0}".format(question) + "Answer:{0}".format(answer)
            message="Is this a good answer to the question?\n" + question_answer
            button_template = ButtonTemplate(message)
            for mod_type in MODERATION_TYPES:
                MODERATION_PAYLOAD['entities']['tag'][0]['value'] = "{0},{1},{2}".format(
                    mod_type, question_answer, user_id)
                button_template.add_postback(mod_type, json.dumps(MODERATION_PAYLOAD))
            response_message = button_template.get_message()
        else:
            question = "Question:{0}".format(question)
            message="Is this a good question?\n" + question
            button_template = ButtonTemplate(message)
            for mod_type in MODERATION_TYPES:
                MODERATION_PAYLOAD['entities']['tag'][0]['value'] = "{0},{1},{2}".format(mod_type, question, user_id)
                button_template.add_postback(mod_type, json.dumps(MODERATION_PAYLOAD))
            response_message = button_template.get_message()

        # find a moderator
        self.cur.execute("SELECT user_id FROM users WHERE is_mod=TRUE")
        moderators = self.cur.fetchall()
        chosen_mod = random.choice(moderators)[0]
        send_message(int(chosen_mod), response_message)
        return "Your response has been submitted for moderation."

    '''
    def remind_to_answer(self):
        """
        Triggered periodically, to remind a user for an answer.

        :return:
        """
    '''

    def check_for_moderation(self, message, user_id, brainwit):
        """

        :param message:
        :param user_id:
        :param handle:
        :return:
        """
        has_entity, triggers_dict, wit_api_json = brainwit.process_query(message)
        if has_entity and ('intent' in triggers_dict):
            trait = triggers_dict['intent'][0]
            confidence = triggers_dict['intent'][1]
            if trait == 'profanity' and confidence > 0.85:
                response_text = "Sorry we can't send your message as it contains a lot of profanity"
            else:
                m = re.search('\[([0-9]*)\]', message)
                if m is not None:
                    question_id = m.group(1)
                    self.cur.execute("SELECT question FROM question WHERE question_id=%s",
                                                   (question_id,))
                    question = self.cur.fetchone()[0]
                    answer = message.split('[{0}]'.format(question_id))[1].strip()
                else:
                    question = message
                    answer = None

                response_text = self.moderate(user_id, question=question, answer=answer)
        else:
            response_text = 'OK'

        return response_text

