from src.utils.log import log
from src.utils.stats import percentile
import json
from templates.generic import *
from src.utils.feedback import asker_feedback_response, subscription_update_request_feedback,\
    barred_from_platform_response, profanity_warning_response, user_stat_request_feedback


TAGS_DATA = open('data/tags.json').read()
TAGS = json.loads(TAGS_DATA)['tags']

TAG_PAYLOAD = {
    'intent': '',
    'entities': {
        'tag': [
            {
                'value': ''
            }
        ]
    }
}


class User:
    def __init__(self, db):
        """
        Handles user statistics.

        :param db: object for Postgres database.
        """
        self.cur = db.get_cursor()

    def update_karma(self, points, user_id):
        """
        Updates karma points of the users.

        :param points: Karma points to be added to the user.
        :param user_id: The unique facebook id of the user, whose karma is to be updated.
        :return: None
        """
        is_karma_updated = False
        try:
            self.cur.execute("SELECT karma from users WHERE user_id=%s;", (user_id,))
            old_karma = int(self.cur.fetchone()[0])
            new_karma = old_karma + points

            try:
                self.cur.execute("UPDATE users SET karma=%s WHERE user_id=%s", (new_karma, user_id))
                is_karma_updated = True
            except Exception, ex:
                log("Update of karma score failed after successful fetch of old karma. Exception: {0}".format(ex))
                new_karma = old_karma
            finally:
                return new_karma, is_karma_updated
        except Exception, ex:
            log("fetching karma from the database failed. Exception: {0}".format(ex))
            return None, is_karma_updated

    def get_user_statistics(self, user_id):
        """
        Obtain the user statistics like karma points, and percentile ranking of the users.

        :param user_id: The unique facebook id of the user whose statistics is requested.
        :return: Text with statistics embedded in it.
        """
        percentile_standing, karma = None, None
        try:
            karma, percentile_standing = self.get_karma_and_percentile(user_id)
        except Exception, ex:
            log("karma fetch from user with specific id failed. Exception: {0}".format(ex))
        finally:
            return user_stat_request_feedback(percentile_standing, karma)

    def get_karma_and_percentile(self, user_id):
        """
        Return karma and percentile ranking of the user

        :param user_id: The unique facebook id of the user whose statistics is requested.
        :return: (karma, percentile ranking) of the user
        """
        self.cur.execute("SELECT karma from users WHERE user_id=%s;", (user_id,))
        karma = int(self.cur.fetchone()[0])
        self.cur.execute("SELECT karma from users;")
        all_karmas = [x[0] for x in self.cur.fetchall()]
        percentile_standing = percentile(karma, all_karmas)
        return karma, percentile_standing

    def update_subscription(self, user_id, flag):
        """
        Update the subscription status of the users.

        :param user_id: Facebook id of the user whose subscription status is to be updated.
        :param flag: True, means subscription should be made active, False, means subscription should be made inactive.
        :return: Feedback for the subscription update.
        """
        try:
            self.cur.execute("UPDATE users SET subscription=%s WHERE user_id=%s;", (flag, user_id))
        except Exception, ex:
            flag = None
            log("subscription update failed. Exception: {0}".format(ex))
        finally:
            return subscription_update_request_feedback(flag)

    def add_user_if_new(self, user_id):
        """
        Adds the user to the user database if they are not already in it.
        This is done at the beginning ofe every interaction that the user makes with Ubik.

        :param user_id: The unique facebook id of the user interacting with Ubik.
        :return: Feedback message mentioning if the addition was successful or not.
        """
        self.cur.execute(
            "SELECT profanity_count FROM users WHERE user_id=%s", (user_id,)
        )
        user_profanity = self.cur.fetchone()
        if user_profanity is None:
            try:
                self.cur.execute(
                    "INSERT INTO users (user_id) SELECT (%s);",
                    (user_id,))
            except Exception, ex:
                log("Unable to add user to the database if new. Exception:{0}".format(ex))
            finally:
                return "OK"
        elif user_profanity[0] == 5:
            return barred_from_platform_response()
        else:
            return "OK"

    def profanity_found(self, user_id):
        """
        Triggers when the profanity is validated in the user message. Updates profanity count in the user db.

        :param user_id: The unique user id of the user who is accused of profanity.
        :return: Feedback message
        """
        self.cur.execute(
            "SELECT profanity_count FROM users WHERE user_id=%s", (user_id,)
        )
        profanity_count = self.cur.fetchone()[0]
        if profanity_count < 5:
            profanity_count += 1
            self.cur.execute(
                "UPDATE users SET profanity_count=%s WHERE user_id=%s", (profanity_count, user_id)
            )
            return profanity_warning_response(profanity_count)
        else:
            return barred_from_platform_response()

    def get_current_answering_question(self, user_id):
        """
        Returns the question that the user is current answering.

        :param user_id: Unique facebook id of the user who is answering the question
        :return: question user is answering.
        """
        try:
            self.cur.execute("SELECT answering_questions FROM users WHERE user_id=%s", (user_id,))
            qid = self.cur.fetchone()[0]
            self.cur.execute("SELECT question FROM question WHERE question_id=%s", (int(qid[0]),))
            question = self.cur.fetchone()[0]
            return question
        except Exception, ex:
            log("Failed to fetch current answering Question. Exception -> {0}".format(ex))
            return None

    @staticmethod
    def send_tags_to_add():
        """
        Sends the tag suggestions, the user can add to their profile.

        :return: Buttons, containing the tags.
        """
        generic_template = GenericTemplate()
        TAG_PAYLOAD['intent'] = 'tag_add'
        for tag in TAGS:
            button = ButtonTemplate("Subscribe")
            TAG_PAYLOAD['entities']['tag'][0]['value'] = tag
            button.add_postback("Subscribe", json.dumps(TAG_PAYLOAD))
            generic_template.add_element(title=tag, buttons=button.get_buttons())

        return generic_template.get_message()

    def send_tags_to_remove(self, user_id):
        """
        Sends the tags that the user is currently subscribed to.

        :param user_id: unique facebook id of the user who requested tag removal.
        :return: buttons, containing the tags.
        """
        self.cur.execute("SELECT skills FROM users WHERE user_id=%s", (user_id,))
        tags = self.cur.fetchone()[0]
        if tags:
            generic_template = GenericTemplate()
            TAG_PAYLOAD['intent'] = 'tag_remove'
            for tag in tags:
                button = ButtonTemplate("Remove")
                TAG_PAYLOAD['entities']['tag'][0]['value'] = tag
                button.add_postback("Remove", json.dumps(TAG_PAYLOAD))
                generic_template.add_element(title=tag, buttons=button.get_buttons())
            return generic_template.get_message()
        else:
            return "No tags found."

    def add_tag(self, tag, user_id):
        """
        Add a given tag to the user profile.

        :param tag: The skill tag that the user will possess now on.
        :param user_id: unique facebook id of the user who requested tag removal.
        :return: None
        """
        try:
            self.cur.execute("UPDATE users SET skills = array_append(skills, %s)"
                             " WHERE user_id=%s AND NOT skills @> ARRAY[%s::TEXT];",
                             (tag, user_id, tag))
        except Exception, ex:
            log('Tag Addition Failed. Exception -> {0}'.format(ex))

    def remove_tag(self, tag, user_id):
        """
        Remove a given tag from the user profile
        :param tag: The skill that will be removed from the user from now.
        :param user_id: unique facebook id of the user who requested tag removal.
        :return: None
        """
        try:
            self.cur.execute("UPDATE users SET skills = array_remove(skills, %s) WHERE user_id=%s;",
                             (tag, user_id))
        except Exception, ex:
            log('Tag Removal Failed. Exception -> {0}'.format(ex))

    def get_profile(self, user_id):
        """
        Get the user profile

        :param user_id: unique facebook id of the user who requested tag removal.
        :return: String containing User profile.
        """
        try:
            self.cur.execute("SELECT karma, skills, profanity_count, subscription FROM users WHERE user_id=%s",
                             (user_id,))
            karma, skills, profanity_count, subscription = self.cur.fetchone()
            _, percentile_standing = self.get_karma_and_percentile(user_id)
            return "* Karma Score: {0}\n* Percentile Ranking: {1}\n* Skill Set: {2}\n*Subscription Status: {3}".\
                format(karma, percentile_standing, skills, subscription)
        except Exception, ex:
            log("Profile Fetch Failed from User DB. Exception:{0}".format(ex))
            return ""










