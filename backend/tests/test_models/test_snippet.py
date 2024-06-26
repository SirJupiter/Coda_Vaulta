#!/usr/bin/python3
"""
Module contains unittest for snippet.py

Setup Test Environment:
Import necessary modules and configure a test database if your model interacts
 with a database.

Test Snippet Creation:
Verify that a Snippet object can be created with valid arguments.

Test Invalid Inputs:
Check that the appropriate exceptions are raised for invalid inputs
 such as empty strings for required fields.

Test Attribute Assignments:
Ensure that all attributes are correctly assigned during object creation.

Test Default Values:
Confirm that default values for created_at and updated_at
 are applied correctly.
"""
import unittest
from datetime import datetime
from models.snippet import Snippet


class TestSnippetModel(unittest.TestCase):

    def test_snippet_creation_success(self):
        """Test successful creation of a Snippet object."""
        snippet = Snippet(
            title="Test Title",
            code="print('Hello, World!')",
            description="A simple print statement",
            language="Python", user_id="1"
        )
        self.assertIsInstance(snippet, Snippet)

    def test_snippet_creation_without_title(self):
        """Test Snippet creation fails without a title."""
        with self.assertRaises(ValueError):
            Snippet(
                title="",
                code="print('Hello, World!')",
                description="A simple print statement",
                language="Python",
                user_id="1"
            )

    def test_snippet_creation_without_code(self):
        """Test Snippet creation fails without code."""
        with self.assertRaises(ValueError):
            Snippet(
                title="Test Title",
                code="",
                description="A simple print statement",
                language="Python",
                user_id="1"
            )

    def test_snippet_creation_without_language(self):
        """Test Snippet creation fails without specifying a language."""
        with self.assertRaises(ValueError):
            Snippet(
                title="Test Title",
                code="print('Hello, World!')",
                description="A simple print statement",
                language="",
                user_id="1"
                )

    def test_attribute_assignments(self):
        """Test that all attributes are correctly assigned."""
        snippet = Snippet(
            title="Test Title",
            code="print('Hello, World!')",
            description="A simple print statement",
            language="Python",
            user_id="1"
            )

        self.assertEqual(snippet.title, "Test Title")
        self.assertEqual(snippet.code, "print('Hello, World!')")
        self.assertEqual(snippet.description, "A simple print statement")
        self.assertEqual(snippet.language, "Python")
        self.assertEqual(snippet.user_id, "1")
        self.assertIsInstance(snippet.created_at, datetime)
        self.assertIsInstance(snippet.updated_at, datetime)

    def test_default_values(self):
        """Test the default values for created_at and updated_at."""
        snippet = Snippet(
            title="Test Title",
            code="print('Hello, World!')",
            description="A simple print statement",
            language="Python",
            user_id="1"
            )
        self.assertIsNotNone(snippet.created_at)
        self.assertIsNotNone(snippet.updated_at)


if __name__ == '__main__':
    unittest.main()
