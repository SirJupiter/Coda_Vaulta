#!/usr/bin/python3
"""
Module contains test for Storage class

The tests are organized into two main classes:

TestUserModel:
Focuses on testing operations related to the User model.
It includes tests for creating and deleting user records in the database.

TestSnippetModel:
Dedicated to testing the Snippet model.
It verifies the creation and deletion of snippet records,
 ensuring that snippets are correctly associated with users and that their
 properties are accurately stored and retrieved.

 --------------------------------------------------------------------

Setup and Teardown

Database Setup:
Before any tests are run, a test database (test_database.db) is created
  using SQLite.
  This ensures that tests do not interfere with the production or
  development databases.

Session Management:
A scoped session (Session) is used for
  database interactions, providing a thread-local session for each test.

Table Creation and Deletion:
At the start of each test class (setUpClass), all necessary tables are created
  in the test database. After all tests in the class have run (tearDownClass),
  these tables are dropped to clean up the test environment.

-----------------------------------------------------------------------

Test Cases
User Model Tests:

User Creation:
Verifies that a user can be successfully created and stored in the database.
Checks that the user's attributes (e.g., username, email) are correctly saved.

User Deletion:
Tests the ability to delete a user from the database.
Ensures that the user is no longer retrievable after deletion.
Snippet Model Tests:

Snippet Creation:
Confirms that a snippet can be created, associated with a user,
  and stored in the database.  It checks the snippet's attributes
  (e.g., title, code, language) for correctness.

Snippet Deletion:
Ensures that a snippet can be deleted from the database and verifies that
  the deleted snippet cannot be retrieved afterward.
"""
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base  # Base contains the declarative_base
from models.user import User
from models.snippet import Snippet

TEST_DATABASE_URL = 'sqlite:///test_database.db'

test_engine = create_engine(TEST_DATABASE_URL, echo=True)

Session = scoped_session(sessionmaker(bind=test_engine))


class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create all tables in the test database
        Base.metadata.create_all(test_engine)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables in the test database
        Base.metadata.drop_all(test_engine)

    def setUp(self):
        self.session = Session()
        self.user = User(
            username="Comfort Shingange",
            email="comfort@example.com",
            password="password123"
            )

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Snippet).delete()
        self.session.commit()
        self.session.close()

    def test_user_creation(self):
        self.session.add(self.user)
        self.session.commit()
        retrieved_user = self.session.query(User).filter_by(
            username="Comfort Shingange").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "Comfort Shingange")
        self.assertEqual(retrieved_user.email, "comfort@example.com")

    def test_user_deletion(self):
        self.session.add(self.user)
        self.session.commit()
        self.session.delete(self.user)
        self.session.commit()
        retrieved_user = self.session.query(User).filter_by(
            username="Comfort Shingange").first()
        self.assertIsNone(retrieved_user)


class TestSnippetModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create all tables in the test database
        Base.metadata.create_all(test_engine)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables in the test database
        Base.metadata.drop_all(test_engine)

    def setUp(self):
        self.session = Session()
        self.user = User(
            username="AlAmeen Adeyemi",
            email="alameeen@example.com",
            password="snippet123"
            )

        self.session.add(self.user)
        self.session.commit()
        self.snippet = Snippet(
            title="Python Snippet",
            code="print('Hello, World!')",
            description="A simple print statement",
            language="Python",
            user_id=self.user.user_id
            )

    def tearDown(self):
        self.session.query(Snippet).delete()
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def test_snippet_creation(self):
        self.session.add(self.snippet)
        self.session.commit()
        retrieved_snippet = self.session.query(Snippet).filter_by(
            title="Python Snippet").first()
        self.assertIsNotNone(retrieved_snippet)
        self.assertEqual(retrieved_snippet.title, "Python Snippet")
        self.assertEqual(retrieved_snippet.code, "print('Hello, World!')")
        self.assertEqual(retrieved_snippet.language, "Python")

    def test_snippet_deletion(self):
        self.session.add(self.snippet)
        self.session.commit()
        self.session.delete(self.snippet)
        self.session.commit()
        retrieved_snippet = self.session.query(Snippet).filter_by(
            title="Python Snippet").first()
        self.assertIsNone(retrieved_snippet)


if __name__ == '__main__':
    unittest.main()
