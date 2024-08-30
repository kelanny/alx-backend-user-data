#!/usr/bin/env python3
"""
This module provides the filter_datum function
to obfuscate specified fields in a log message.
"""

import re
from typing import List


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
