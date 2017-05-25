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
from src.utils.fb_api.send import send_message
from src.utils.feedback import asker_feedback_response, useless_message_response, answer_feedback_to_answerer
from src.utils.log import log


class PostbackEvent:

    def __init__(self, db_handle):
        """
        Event handler for handling event tiggers like Question being asked, Answer being given, feedback being posted.

        :param db_handle: handle for Postgres database.
        """
        self.cur = db_handle.database().get_cursor()
        self.question_handler = db_handle.question()
        self.answer_handler = db_handle.answer()
        self.user_handler = db_handle.user()

    def handle_postback(self, postback_payload, user_id):
        """
        Handles following feedback:
        1. Moderation
        2. Rating of answer
        3. Add Tags
        4. Remove Tags

        :param postback_payload: The postback payload provided with the postback event.
        :param user_id: The unique user id of the user who will receive the feedback
        :return: feedback for the user
        """
        data = json.loads(postback_payload)
        if data['intent'] == 'moderation':
            self.moderation_update(data['entities']['tag'][0]['value'])
            response = "Thanks"
        elif data['intent'] == 'rating':
            response = self.answer_rating_update(data['entities']['tag'][0]['value'])
        elif data['intent'] == 'tag_add':
            response = self.user_handler.add_tag(data['entities']['tag'][0]['value'], user_id)
        elif data['intent'] == 'tag_remove':
            response = self.user_handler.remove_tag(data['entities']['tag'][0]['value'], user_id)
        else:
            log("Invalid Postback Intent -> {0}".format(data['intent']))
            response = None

        return response

    def moderation_update(self, payload):
        """
        Handles different types of moderation response provided by the moderator,
        and responds to the asker / answerer with appropriate feedback.
        :param payload: Moderation payload (response, data, user_id of the asker / answerer)
        :return: None
        """
        response, data, user_id = [x.strip() for x in payload.split(',')]
        mod_feedback = None
        if response == "YES":
            if 'Answer:' in data:
                mod_feedback = self.answer_handler.add_answer('done', user_id)
            elif data.startswith('Question:'):
                mod_feedback = self.question_handler.add_question(data[9:], user_id)
        elif response == "NO":
            mod_feedback = useless_message_response(data)
        elif response == "PROFANE":
            mod_feedback = self.user_handler.profanity_found(user_id) + "\nFor:{0}".format(data)

        send_message(user_id, mod_feedback)

    def answer_rating_update(self, payload):
        """
        Sends feedback to the answerer after updating its karma, when the asker rates the answer.
        :param payload: Answer rating payload (points, rating, answerer_id, question_id, question) in string format.
        :return:
        """
        points, rating, answerer_id, question_id, question = [x.strip() for x in payload.split(',')]
        if rating == 'OOW':
            self.question_handler.mark_question_as_resolved(int(question_id))
        karma, is_karma_updated = self.user_handler.update_karma(int(points), answerer_id)
        try:
            if is_karma_updated:
                respond_message = answer_feedback_to_answerer(rating, question, karma)
                send_message(int(answerer_id), respond_message)
        except Exception, ex:
            log("failed sending feedback response to responder. Exception:{0}".format(ex))

        return asker_feedback_response(is_karma_updated) # @TODO: Not sure if this line is important
