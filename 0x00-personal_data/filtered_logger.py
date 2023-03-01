#!/usr/bin/env python3
import logging
import mysql.connector
import re
from typing import List
from os import environ


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    function called filter_datum that returns the log message obfuscated

    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
               fields in the log line (message)

    """
    for field in fields:
        pattern = field + '=' + r'(.*?)' + separator
        message = re.sub(pattern, field + '=' + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """ Function to log user data """
    logging.Logger(name='user_data').setLevel(logging.INFO)
    logger = logging.getLogger('user_data')
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Creates a connector object to a database """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=db_host,
        database=db_name)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def main() -> None:
    """ Function to retrieve logs from database """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    headers = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        message = ''
        for f, p in zip(row, headers):
            message += f'{p}={(f)};'
        log_record = logging.LogRecord("user_data", logging.INFO, None, None,
                                       message, None, None)
        formatter = RedactingFormatter(fields=headers)
        print(formatter.format(log_record))

    cursor.close()
    db.close()

if __name__ == '__main__':
    main()
