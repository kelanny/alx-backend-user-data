#!/usr/bin/env python3
"""
This module provides the filter_datum function
to obfuscate specified fields in a log message.
"""

import mysql.connector
from mysql.connector import connection
import logging
from typing import List
import os
import re


PII_FIELDS = ("name", "email", "phone_number", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """ Initializes the RedactingFormatter object
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formats the record
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return (super(RedactingFormatter, self).format(record))


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the values of specified fields in the log message.

    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log message.
        separator (str): The character separating fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=.*?(?={separator}|$)"
    return (re.sub(pattern, lambda x: f"{x.group(1)}={redaction}", message))


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger that handles PII fields.

    Returns:
        logging.Logger: Configured logger for user data.
    """
    # Create a logger named "user_data"
    logger = logging.getLogger("user_data")

    # Set the logging level to INFO (only log msgs with this level or higher)
    logger.setLevel(logging.INFO)

    # Prevent the logger from propagating messages to other loggers
    logger.propagate = False

    # Create a StreamHandler to send log messages to the console
    stream_handler = logging.StreamHandler()

    # Create an instance of RedactingFormatter, passing appropriate arguments
    formatter = RedactingFormatter(fields=PII_FIELDS)

    # Set the formatter for the StreamHandler
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the logger
    logger.addHandler(stream_handler)

    return (logger)


def get_db() -> connection.MySQLConnection:
    """
    Connects to a secure database using credentials from environment variables.

    Returns:
        connection.MySQLConnection: Database connection object.
    """
    # Retrieve database credentials from environment variables with defaults
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Create a connection to the database
    return (
        mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
    )
