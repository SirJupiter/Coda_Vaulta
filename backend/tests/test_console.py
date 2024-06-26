#!/usr/bin/python3
"""
Module contains unittest for console.py

Setup and Teardown Methods:

Setup: Create a CODAVAULTAConsole instance for use in tests.
Teardown: Clean up any resources or mock patches after each test.

------------------------------------------------------------------

Tests for do_create Method:

Test creating a new user with valid arguments.
Test creating a new snippet with valid arguments and an existing user.
Test creating a snippet with a non-existing user.
Test creating an instance of a non-existing class.

------------------------------------------------------------------

Tests for do_show Method:

Test showing an instance with no class name provided.
Test showing an instance of a non-existing class.
Test showing a user that does not exist.
Test showing a snippet that does not exist.
Test showing an existing user.
Test showing an existing snippet.

-------------------------------------------------------------------

Mocking Database Calls:

Use of unittest.mock.patch to mock database interactions
 to avoid actual database calls, focusing on the logic of console.py.
"""

import unittest
from unittest.mock import patch, MagicMock
from console import CODAVAULTAConsole
# from models.snippet import Snippet
# from models.engine.storage import Storage
import io


class TestCODAVAULTAConsole(unittest.TestCase):

    def setUp(self):
        self.cli = CODAVAULTAConsole()

    def test_do_create_user_valid(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("create User name='John_Doe' \
                            email='john@example.com'")
            self.assertNotEqual(fake_out.getvalue().strip(),
                                "** class doesn't exist **")

    def test_do_create_snippet_non_existing_user(self):
        with patch('console.models.storage.get_user_by_user_id',
                   return_value=None):
            with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
                self.cli.onecmd(
                    "create Snippet Test print(\"Hello\") \
                        Test-snippet python non_existing")
                self.assertIn("** user doesn't exist **",
                              fake_out.getvalue().strip())

    def test_do_create_non_existing_class(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("create NonExistingClass")
            self.assertIn("** class doesn't exist **",
                          fake_out.getvalue().strip())

    def test_do_show_no_args(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("show")
            self.assertIn("** class name missing **",
                          fake_out.getvalue().strip())

    def test_do_show_class_not_exist(self):
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("show NonExistentClass")
            self.assertIn("** class doesn't exist **",
                          fake_out.getvalue().strip())

    @patch('console.models.storage.get_user_by_user_id')
    def test_do_show_user_not_found(self, mock_get_user):
        mock_get_user.return_value = None
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("show User non_existing_id")
            self.assertIn("** no instance found **",
                          fake_out.getvalue().strip())

    @patch('console.models.storage.get_snippet_by_snippet_id')
    def test_do_show_snippet_not_found(self, mock_get_snippet):
        mock_get_snippet.return_value = None
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("show Snippet non_existing_id")
            self.assertIn("** no instance found **",
                          fake_out.getvalue().strip())

    @patch('console.models.storage.get_user_by_user_id')
    def test_do_show_user_found(self, mock_get_user):
        mock_user = MagicMock()
        mock_user.to_dict.return_value = {'id': 'user_id', 'name': 'Test-User'}
        mock_get_user.return_value = mock_user
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("show User user_id")
            self.assertIn('Test-User', fake_out.getvalue().strip())

    @patch('console.models.storage.get_snippet_by_snippet_id')
    def test_do_show_snippet_found(self, mock_get_snippet):
        mock_snippet = MagicMock()
        mock_snippet.to_dict.return_value = {
            'id': 'snippet_id',
            'title': 'Test-Snippet'
            }
        mock_get_snippet.return_value = mock_snippet
        with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
            self.cli.onecmd("show Snippet snippet_id")
            self.assertIn('Test-Snippet', fake_out.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
