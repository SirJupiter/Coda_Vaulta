#!/usr/bin/python3
"""Module containers validators and hashing function"""

from datetime import datetime
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


def get_ordinal_suffix(day):
    """Return ordinal suffix for the day, e.g., 'th', 'rd', 'nd', 'st'."""
    if 10 <= day <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return suffix


def format_datetime(dt_input):
    """
    Format datetime object or ISO format string to
    '12th May 2024 at 22:45' format.
    """
    # Check if dt_input is a string, then parse it
    if isinstance(dt_input, str):
        try:
            dt = datetime.fromisoformat(dt_input)
        except ValueError:
            raise ValueError("String input must be in ISO format")
    elif isinstance(dt_input, datetime):
        dt = dt_input
    else:
        raise TypeError("Must be a datetime object or a string in ISO format")

    # Extract the day and determine its ordinal suffix
    day = dt.day
    ordinal_suffix = get_ordinal_suffix(day)

    # Format the datetime object, manually inserting the ordinal suffix
    formatted_date = dt.strftime(f'%-d{ordinal_suffix} %B %Y at %H:%M')
    return formatted_date
