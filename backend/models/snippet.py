#!/usr/bin/python3
"""Module contains Snippet class from which snippets can be instantiated"""

from datetime import datetime
from uuid import uuid4
from models.base import Base
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
# from sqlalchemy.orm import relationship


class Snippet(Base):
    """Class for creating new snippets

    Class Attribute:
        number_of_snippets (int): number of created snippets

    Instance Attributes:
        snippet_id (str): id of created snippet
        title (str): title of snippet
        code (text): code to be formatted into snippet
        language (str): language of code to be formatted
        description (str): description of the code
        created_at (datetime): time snippet was created
        updated_at (datetime): time snippet was edited/updated
        user_id (int): id of user of the current account
    """

    __tablename__ = 'snippets'

    snippet_id = Column(String(60), primary_key=True)
    title = Column(String(60), nullable=False)
    description = Column(String(60), nullable=True)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(String(60), ForeignKey('users.user_id'), nullable=False)

    number_of_snippets = 0

    def __init__(self, title, code, description, language, user_id):
        """Creates a snippet object at instantiation

        Args:
            title (str): title of snippet
            code (str): code to be made into a snippet
            description (str): description of the code snippet
            user_id (int): id of user
        """
        if not title:
            raise ValueError('Title cannot be empty')
        if not code:
            raise ValueError('Code cannot be empty')
        if not language:
            raise ValueError('Language cannot be empty')
        if not user_id:
            raise ValueError('User_id must be present')

        self.snippet_id = str(uuid4())
        self.title = title
        self.description = description
        self.language = language
        self.code = code
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        Snippet.number_of_snippets += 1

    def __repr__(self):
        """Returns a string representation of the object"""
        return f"Snippet({self.snippet_id}, {self.title}, {self.code})"

    def save(self):
        """Saves snippet object to database"""
        from models.engine.storage import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes snippet object from database"""
        from models.engine.storage import storage
        storage.delete(self)

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    @classmethod
    def all(cls):
        """Returns all user objects from database"""
        from models.engine.storage import storage
        return storage.all(cls)

    @classmethod
    def count(cls):
        """Returns number of user objects in database"""
        from models.engine.storage import storage
        return len(storage.all(cls))

    @classmethod
    def clear_all(cls):
        """Deletes all user objects from database"""
        from models.engine.storage import storage
        storage.delete_all(cls)
