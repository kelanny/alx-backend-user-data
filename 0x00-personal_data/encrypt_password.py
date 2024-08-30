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
