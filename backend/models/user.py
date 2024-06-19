#!/use/bin/python3
"""Module contains User class from which users can be instantiated"""

from datetime import datetime
from uuid import uuid4
from utilities import validate_username, validate_email, password_hash
from models.base import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    """User class

    Class Attribute:
        number_of_users (int): number of users that exist

    Instance Attributes:
        user_id (str): unique user id
        username (str): name of user
        email (str): email address
        hashed_password (str): password
        created_at (datetime): time user account was created
    """

    __tablename__ = 'users'

    user_id = Column(String(60), primary_key=True)
    username = Column(String(60), unique=True, nullable=False)
    email = Column(String(60), unique=True, nullable=False)
    hashed_password = Column(String(60), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    snippets = relationship('Snippet', backref='users',
                            cascade='all, delete-orphan')

    number_of_users = 0

    def __init__(self, username, email, password):
        """Creates a user object at instantiation

        Args:
            user_id (str): unique id of a registered user
            created_at (datetime): time user account was created
        """
        self.user_id = str(uuid4())
        self.username = username
        self.email = email
        self.hashed_password = password_hash(password)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        validate_username(username)
        validate_email(email)

        User.number_of_users += 1

    def __repr__(self):
        """Returns a string representation of the object"""
        return f"User({self.user_id}, {self.username}, {self.email})"

    def save(self):
        """Saves user object to database"""
        from models.engine.storage import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """Deletes user object from database"""
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

    @classmethod
    def get_by_id(user_id):
        """Returns user object from database based on user_id"""
        from models.engine.storage import storage
        return storage.get_user_by_user_id(user_id)

    @classmethod
    def get_by_username(username):
        """Returns user object from database based on username"""
        from models.engine.storage import storage
        return storage.get_user_by_username(username)

    @classmethod
    def get_by_email(email):
        """Returns user object from database based on email"""
        from models.engine.storage import storage
        return storage.get_user_by_email(email)
