from src.utils.log import log
from src.event.databaseEvent import DatabaseEvent
from src.utils.feedback import question_save_feedback


class Question:
    def __init__(self, db):
        """
        Handles questions posted to the Ubik platform.

        :param db: object for Postgres database.
        """
        self.cur = db.get_cursor()

    def add_question(self, question, asker_id):
        """
        Adds the question to the database

        :param question: The test of the question
        :param asker_id: The person who asked the question
        :return: None
        """
        is_question_stored = False
        try:
            self.cur.execute(
                "INSERT INTO questions (question, asker_id, has_answer) VALUES (%s, %s, %s) RETURNING question_id;",
                (question, str(asker_id), False))
            question_id = self.cur.fetchone()[0]
            is_question_stored = True
            DatabaseEvent.new_question(question_id, question, asker_id)
        except Exception, ex:
            log("Failed to insert question in the database. Exception thrown: {0}".format(ex))

        return question_save_feedback(is_question_stored)

    def mark_question_as_resolved(self, question_id):
        """
        If the user adds OOW to a question's answer, then the question is marked as resolved.
        The user will not get any further answers for that question.
        :param question_id: The question's unique id.
        :return: None
        """
        try:
            self.cur.execute(
                "UPDATE questions SET has_answer=TRUE WHERE question_id=%s",
                (question_id,)
            )
        except Exception, ex:
            log("question resolution db update failed. Exception thrown: {0}".format(ex))

