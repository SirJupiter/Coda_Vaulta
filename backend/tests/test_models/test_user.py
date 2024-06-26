#!/usr/bin/python3
"""Module contains unittest for the User model"""

import os
import unittest
from dotenv import load_dotenv
from unittest.mock import patch
from models.user import User
from datetime import datetime


# Move up two levels from the current file directory
# then specify the path to test.env
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'test.env')

# Load environment variables from test.env
load_dotenv(dotenv_path=dotenv_path)


class TestUserModel(unittest.TestCase):
    def setUp(self):
        """
        Setup method to create a user object before each test.
        Each test is using environment variables.
        """

        test_username = os.environ.get(
            'TEST_USER_USERNAME', 'default testuser')
        test_email = os.environ.get('TEST_USER_EMAIL', 'test_user@example.com')
        test_password = os.environ.get('TEST_USER_PASSWORD', 'TestPassword123')

        self.username = test_username
        self.email = test_email
        self.password = test_password
        self.user = User(self.username, self.email, self.password)

    def tearDown(self):
        """Tear down method to delete the user object after each test"""
        del self.user

    def test_user_creation(self):
        """Test user object is created with correct attributes"""
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        # Assuming password_hash returns a hash of the password
        self.assertNotEqual(self.user.hashed_password, self.password)
        self.assertTrue(isinstance(self.user.created_at, datetime))
        self.assertTrue(isinstance(self.user.updated_at, datetime))

    def test_user_representation(self):
        """Test the __repr__ method returns the expected string"""
        ex_repr = f"User({self.user.user_id}, {self.username}, {self.email})"
        self.assertEqual(repr(self.user), ex_repr)

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method calls storage's new and save methods"""
        self.user.save()
        mock_storage.new.assert_called_once_with(self.user)
        mock_storage.save.assert_called_once()

    @patch('models.storage')
    def test_delete_method(self, mock_storage):
        """Test the delete method calls storage's delete method"""
        self.user.delete()
        mock_storage.delete.assert_called_once_with(self.user)

    def test_user_count_increment(self):
        """Test that the user count increments upon creating a new user"""
        initial_count = User.number_of_users
        new_user = User("new user", "new_user@example.com", "NewPassword123")
        self.assertEqual(User.number_of_users, initial_count + 1)
        del new_user  # Clean up

    @patch('models.user.validate_username')
    @patch('models.user.validate_email')
    def test_user_validation(
            self, mock_validate_email, mock_validate_username):
        """Test that username and email validation functions are called
        These functions are already called in setUp,
        so we check they were called again.
        """
        new_user = User(
            "another user", "another_user@example.com", "AnotherPassword123")
        mock_validate_username.assert_called_with("another user")
        mock_validate_email.assert_called_with("another_user@example.com")
        del new_user  # Clean up


if __name__ == '__main__':
    unittest.main()
