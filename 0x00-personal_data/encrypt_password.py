#!/usr/bin/env python3
"""Hash password module for encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a random salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Generate a salt for the password
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return (hashed_password)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to validate.

    Returns:
        bool: True if the pass matches hashed, False otherwise.
    """
    return (bcrypt.checkpw(password.encode('utf-8'), hashed_password))
