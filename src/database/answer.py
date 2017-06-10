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
import re
from src.utils.feedback import answer_save_feedback, finish_present_answer_feedback, response_not_requested_feedback,\
    answer_cancelled_feedback
from src.utils.log import log


class Answer:
    def __init__(self, db):
        """
        Handles answers posted to the Ubik platform.

        :param db: object for Postgres database.
        """
        self.cur = db.get_cursor()

    def add_answer(self, answer, responder_id):
        """
        Adds the answer to the database.

        :param answer: The answer sent by the responder
        :param responder_id: The unique facebook id of the responder of the answer.
        :return: Feedback response for answer message.
        """
        m = re.search('\[([0-9]*)\]', answer)
        try:
            question_id = m.group(1)
        except Exception, ex:
            log("Exception Occured -> {0}".format(ex))
            question_id = None

        if question_id is not None:
            return self.answer_begins_response(question_id, answer, responder_id)

        elif answer.lower() == "done":
            return self.done_answering_response(responder_id)

        elif answer.lower() == "cancel":
            return self.cancel_present_answer(responder_id)
        else:
            self.append_to_present_answer(answer, responder_id)
            return 'NULL'

    def answer_begins_response(self, question_id, answer, responder_id):
        """
        Handles the answer message, which has just begin to be answered by the responder.

        :param question_id: The question id of the question being answered.
        :param answer: The answer text, that the user is sending.
        :param responder_id: The unique facebook id of the user answering the question.
        :return: Feedback text mentioning how to answer.
        """
        self.cur.execute("SELECT answering_buffer FROM users WHERE user_id=%s "
                         "AND sent_questions @> ARRAY[%s::INT];",
                         (responder_id, question_id))
        answer_buffer = self.cur.fetchone()
        if not answer_buffer:
            return response_not_requested_feedback(question_id)
        else:
            if answer_buffer[0] != '':
                return finish_present_answer_feedback(question_id)
            else:
                answer_buffer = answer_buffer[0]
                answer_buffer += "\n{0}".format(answer)
                self.cur.execute("UPDATE users SET answering_buffer=%s WHERE user_id=%s", (answer_buffer, responder_id))

                self.cur.execute("UPDATE users SET answering_questions = array_append(answering_questions, %s)"
                                 " WHERE user_id=%s AND NOT answering_questions @> ARRAY[%s::INT];",
                                 (question_id, responder_id, question_id))

                self.cur.execute("UPDATE users SET sent_questions = array_remove(sent_questions, %s)"
                                 " WHERE user_id=%s;",
                                 (question_id, responder_id))
                return "*Type 'done' when you are finished writing the answer\n" \
                       "* Type 'cancel' if you wish to cancel your answer\n"

    def done_answering_response(self, responder_id, db_event_handler):
        """
        Triggers when the responder is done answering a question.

        :param responder_id: The unique facebook id of the user answering the question.
        :return: Feedback response, mentioning that the question is saved.
        """
        self.cur.execute("SELECT answering_buffer FROM users WHERE user_id=%s", (responder_id,))
        answer = self.cur.fetchone()[0]
        m = re.search('\[([0-9]*)\]', answer)
        question_id = m.group(1)
        answer_text = answer.split('[{0}]'.format(question_id))[1].strip()

        self.cur.execute(
            "INSERT INTO answer (answer, responder_id, question_id) VALUES (%s, %s, %s);",
            (answer_text, responder_id, question_id))
        answer_stored = True
        self.cur.execute("UPDATE users SET answered_questions = array_append(answered_questions, %s)"
                         " WHERE user_id=%s AND NOT answered_questions @> ARRAY[%s::INT];",
                         (question_id, responder_id, question_id))

        self.cur.execute("UPDATE users SET answering_questions = array_remove(answering_questions, %s)"
                         " WHERE user_id=%s;",
                         (question_id, responder_id))
        self.cur.execute("UPDATE users SET answering_buffer=%s WHERE user_id=%s", ('', responder_id))
        db_event_handler.new_answer(question_id, answer_text, responder_id)
        return answer_save_feedback(answer_stored)

    def cancel_present_answer(self, responder_id):
        """
        Handles the case when the user, does not want to answer the question anymore.

        :param responder_id: The unique facebook id of the user answering the question.
        :return: Feedback message, saying that the answer is indeed cancelled.
        """
        self.cur.execute("SELECT answering_buffer FROM users WHERE user_id=%s", (responder_id,))
        answer_buffer = self.cur.fetchone()[0]
        m = re.search('\[([0-9]*)\]', answer_buffer)
        question_id = m.group(1)
        self.cur.execute("UPDATE users SET sent_questions = array_append(sent_questions, %s)"
                         " WHERE user_id=%s AND NOT sent_questions @> ARRAY[%s::INT];",
                         (question_id, responder_id, question_id))

        self.cur.execute("UPDATE users SET answering_questions = array_remove(answering_questions, %s)"
                         " WHERE user_id=%s;",
                         (question_id, responder_id))
        self.cur.execute("UPDATE users SET answering_buffer=%s WHERE user_id=%s", ('', responder_id))
        return answer_cancelled_feedback(question_id)

    def append_to_present_answer(self, answer, responder_id):
        """
        Handles the case, when the user is in mid of answering a question, after first trigger of response.
        :param answer: The answer text to be appended to the present answer.
        :param responder_id: The unique facebook id of the user answering the question.
        :return: None
        """
        self.cur.execute("SELECT answering_buffer FROM users WHERE user_id=%s", (responder_id,))
        answer_buffer = self.cur.fetchone()[0]
        answer_buffer += "\n{0}".format(answer)
        self.cur.execute("UPDATE users SET answering_buffer=%s WHERE user_id=%s", (answer_buffer, responder_id))


