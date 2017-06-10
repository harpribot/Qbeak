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
import os
import config
import requests
from src.utils.feedback import joke_response, wiki_response, confusion_response, help_response, bye_response,\
    greeting_response, sample_examples_response, about_response, quotes_response, motivations_response,\
    puzzles_response, facts_response, question_answer_help_response

WIT_AI_ACCESS_TOKEN = os.environ.get('WIT_AI_ACCESS_TOKEN', config.WIT_AI_ACCESS_TOKEN)


class BrainWit:
    def __init__(self, db_handle, event_handle):
        self.question_handler = db_handle.question()
        self.answer_handler = db_handle.answer()
        self.user_handler = db_handle.user()
        self.db_event_handler = event_handle.database()
        self.postback_event_handler = event_handle.postback()

    @staticmethod
    def process_query(message):
        """
        Processes query and returns Intent Trait, Trait Confidence, and Boolean value=True if trait present, else False
        :param message: The incoming message passed to the wit.ai platform
        :return: Tuple(has_intent, intent_dict, confidence)
        """
        r = requests.get('https://api.wit.ai/message?v=20170419&q=' + message, headers={
            'Authorization': 'Bearer %s' % WIT_AI_ACCESS_TOKEN
        })
        wit_api_json = r.json()
        has_entity = bool(wit_api_json['entities'])
        if has_entity:
            triggers = wit_api_json['entities'].keys()
            triggers_dict = {x: (wit_api_json['entities'][x][0]['value'],
                                 wit_api_json['entities'][x][0]['confidence']) for x in triggers}
            return has_entity, triggers_dict, wit_api_json
        return has_entity, None, wit_api_json

    def get_response(self, sender_id, message):
        """
        Get response from BrainWit NLP engine running Wit.ai on backend
        :param sender_id: The unique facebook id of the person sending the message
        :param message: The message payload sent by the sender.
        :return: response text to be sent.
        """
        has_entity, triggers_dict, wit_api_json = BrainWit.process_query(message)

        if not has_entity:
            if message.endswith('?'):
                response = self.question_handler.add_question(message, sender_id, self.db_event_handler)
            else:
                response = confusion_response()
        elif 'intent' in triggers_dict:
            trait = triggers_dict['intent'][0]
            confidence = triggers_dict['intent'][1]
            if trait == 'profanity':
                if confidence > 0.85:
                    response = self.user_handler.profanity_found(sender_id)
                else:
                    if message.endswith('?'):
                        response = self.db_event_handler.check_for_moderation(message, sender_id, self)
                    else:
                        response = confusion_response()

            elif trait == 'greeting' and confidence > 0.8:
                response = greeting_response()
            elif trait == 'examples' and confidence > 0.8:
                response = sample_examples_response()
            elif trait == 'goodbye' and confidence > 0.8:
                response = bye_response()
            elif trait == 'quote' and confidence > 0.8:
                response = quotes_response()
            elif trait == 'fact' and confidence > 0.8:
                response = facts_response()
            elif trait == 'QA' and confidence > 0.8:
                response = question_answer_help_response()
            elif trait == 'motivation' and confidence > 0.8:
                response = motivations_response()
            elif trait == 'puzzle' and confidence > 0.8:
                response = puzzles_response()
            elif trait == 'help' and confidence > 0.8:
                response = help_response()
            elif trait == 'joke' and confidence > 0.8:
                response = joke_response()
            elif trait == 'about' and confidence > 0.8:
                response = about_response()
            elif trait == 'profile' and confidence > 0.8:
                response = self.user_handler.get_profile(sender_id)
            elif trait == 'ranking' and confidence > 0.8:
                response = self.user_handler.get_user_statistics(sender_id)
            elif trait == 'subscription_restart' and confidence > 0.8:
                response = self.db_event_handler.restart_subscription(sender_id)
            elif trait == 'subscription_stop' and confidence > 0.8:
                response = self.db_event_handler.pause_subscription(sender_id)
            elif trait == 'tags_add' and confidence > 0.8:
                response = self.user_handler.send_tags_to_add()
            elif trait == 'tags_remove' and confidence > 0.8:
                response = self.user_handler.send_tags_to_remove(sender_id)
            elif trait == 'wiki' and 'wikipedia_search_query' in triggers_dict and confidence > 0.8:
                search_query = triggers_dict['wikipedia_search_query'][0]
                response = wiki_response(search_query)
            elif trait == 'question' and confidence > 0.8:
                response = self.question_handler.add_question(message, sender_id, self.db_event_handler)
            else:
                if message.endswith('?'):
                    response_text = self.db_event_handler.check_for_moderation(message, sender_id, self)
                    if response_text == "OK":
                        response = self.question_handler.add_question(message, sender_id, self.db_event_handler)
                    else:
                        response = None
                else:
                    response = confusion_response()
        else:
            if message.endswith('?'):
                response = "This question will be moderated. " \
                           "If modertator reports the question, you will lose one life. " \
                           "After losing 5 lives, you will lose access for 2 weeks." + \
                           self.question_handler.add_question(message, sender_id)
            else:
                response = confusion_response()

        return response
