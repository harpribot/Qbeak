import os
import config
import psycopg2
from src.utils.log import *
from src.utils.parser import database_parser

DATABASE_URL = os.environ.get('DATABASE_URL', config.DATABASE_URL)


class Database:
    def __init__(self):
        """
        Database in which question, answers, and user information is posted.
        """
        self.conn = None
        db_user, db_pass, db_host, db_port, db_name = database_parser(DATABASE_URL)
        try:
            self.conn=psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'".
                format(db_name, db_user, db_host, db_port, db_pass))
            self.conn.autocommit = True
        except Exception, ex:
            log("I am unable to connect to the database. Exception: {0}".format(ex))

    def connection_status(self):
        """
        Sends boolean status of the database

        :return: True, if the connection is established, else False
        """
        return self.conn is not None

    def get_cursor(self):
        """
        Sends database cursor, to update the database.

        :return: database cursor.
        """
        return self.conn.cursor()
