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
