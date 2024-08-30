#!/usr/bin/env python3
"""Module to obfuscate sensitive information in log messages."""

import logging
from typing import List
from mysql.connector import connection
from filtered_logger import get_db, get_logger, PII_FIELDS


get_db = __import__('filtered_logger').get_db
get_logger = __import__('filtered_logger').get_logger


def main():
    """
    Retrieves all rows from the 'users' table in the database, filters
    the sensitive information using RedactingFormatter, and logs the
    filtered information.
    """
    # Obtain a database connection
    db = get_db()
    cursor = db.cursor()

    # Query to retrieve all rows from the 'users' table
    query = "SELECT name, email, phone, ssn, password, \
            ip, last_login, user_agent FROM users;"
    cursor.execute(query)

    # Get the logger
    logger = get_logger()

    # Fetch all rows and log each one with filtered PII
    for row in cursor.fetchall():
        # Create a dictionary to map column names to values
        user_data = {
            "name": row[0],
            "email": row[1],
            "phone": row[2],
            "ssn": row[3],
            "password": row[4],
            "ip": row[5],
            "last_login": row[6].strftime('%Y-%m-%d %H:%M:%S'),
            "user_agent": row[7]
        }

        # Format the log message
        log_message = "; ".join(
            [f"{key}={value}" for key, value in user_data.items()]
            )
        logger.info(log_message)

    # Close the cursor and database connection
    cursor.close()
    db.close()


# Ensure the main function runs only if the script is executed directly
if __name__ == "__main__":
    main()
