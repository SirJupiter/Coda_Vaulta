#!/usr/bin/python3
"""Module containers validators and hashing function"""

import re
import bcrypt


def validate_username(username):
    """Validates username passed for account creation

    Args:
        username (str): username

    Raises:
        ValueError: if the username is an empty string
    """
    pattern = r"^[A-Za-z0-9 ]*$"
    if not username:
        raise ValueError('Username cannot be empty')
    if not re.match(pattern, username):
        raise ValueError(
            'Username can only contain alphanumeric characters and spaces')


def validate_email(email):
    """Validates email passed in for account creation

    Args:
        email (str): email address

    Raises:
        ValueError: if the email passed in does not match regex pattern
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError(f'Invalid email address: {email}')


def password_hash(password):
    """Checks and hashes password
        -   Checks if password is empty
        -   Checks is password is less than 8 characters
        -   Generates a saly and then hashes password

    Args:
        password (str): password passed in

    Raises:
        ValueError: if password is empty or is less than 8 chars long

    Returns:
        Hashed password
    """
    if not password:
        raise ValueError('Password cannot be empty')
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def verify_password(password, hashed_password):
    """Checks if provided password matches stored password

    Args:
        password (str): password passed in by user
        hashed_password (str): hashed password stored in database

    Returns:
        True if password and hashed_password match
    """
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
