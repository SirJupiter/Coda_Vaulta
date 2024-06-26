#!/usr/bin/python3
"""
Module contains unittest for utilities.py

Test password_hash Function:
Verify it raises a ValueError for empty or short passwords and
     returns a hashed password for valid inputs.

Test verify_password Function:
Check if it correctly verifies a password against its hashed version.

Test get_ordinal_suffix Function:
Ensure it returns the correct ordinal suffix for a given day.

Test format_datetime Function:
Validate it correctly formats datetime objects and ISO format strings,
    and raises appropriate exceptions for invalid inputs.
"""

import unittest
from utilities import validate_username, validate_email, password_hash
from utilities import verify_password, get_ordinal_suffix, format_datetime
import bcrypt


class TestValidationFunctions(unittest.TestCase):
    # Existing tests for validate_username and validate_email...
    def test_validate_username_with_empty_string(self):
        with self.assertRaises(ValueError) as context:
            validate_username('')
        self.assertTrue('Username cannot be empty' in str(context.exception))

    def test_validate_username_with_invalid_characters(self):
        with self.assertRaises(ValueError) as context:
            validate_username('Invalid Username!')
        self.assertTrue(
            'Username can only contain alphanumeric characters and spaces'
            in str(context.exception))

    def test_validate_email_with_invalid_email(self):
        with self.assertRaises(ValueError) as context:
            validate_email('invalidemail.com')
        self.assertTrue('Invalid email address: invalidemail.com'
                        in str(context.exception))

    def test_password_hash_empty(self):
        with self.assertRaises(ValueError):
            password_hash('')

    def test_password_hash_short(self):
        with self.assertRaises(ValueError):
            password_hash('short')

    def test_password_hash_valid(self):
        password = 'validPassword123'
        hashed = password_hash(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed))

    def test_verify_password(self):
        password = 'testPassword'
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        self.assertTrue(verify_password(password, hashed_password))

    def test_get_ordinal_suffix(self):
        self.assertEqual(get_ordinal_suffix(1), 'st')
        self.assertEqual(get_ordinal_suffix(2), 'nd')
        self.assertEqual(get_ordinal_suffix(3), 'rd')
        self.assertEqual(get_ordinal_suffix(11), 'th')
        self.assertEqual(get_ordinal_suffix(21), 'st')

    def test_format_datetime_with_datetime_object(self):
        from datetime import datetime
        dt = datetime(2024, 5, 12, 22, 45)
        self.assertEqual(format_datetime(dt), '12th May 2024 at 22:45')

    def test_format_datetime_with_iso_string(self):
        dt_iso = '2024-05-12T22:45:00'
        self.assertEqual(format_datetime(dt_iso), '12th May 2024 at 22:45')

    def test_format_datetime_with_invalid_input(self):
        with self.assertRaises(ValueError):
            format_datetime('not-a-datetime')
        with self.assertRaises(TypeError):
            format_datetime(12345)


if __name__ == '__main__':
    unittest.main()
