#!/usr/bin/python3
"""Contains class definition of storage"""

from models.user import User
from models.snippet import Snippet
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from models.engine.db_configs import DB, USER, PASSWORD, HOST
import logging


classes = {
    'User': User,
    'Snippet': Snippet
}

created_engine = f'mysql+mysqldb://{USER}:{PASSWORD}@{HOST}/{DB}'


class Storage:
    """Class definition of storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes storage"""
        self.__engine = create_engine(created_engine, pool_pre_ping=True)
        self.reload()

    def all(self, cls=None):
        """Returns all objects of a specific class in storage"""
        if cls:
            return self.__session.query(classes[cls]).all()
        else:
            result = {}
            for cls_name, value in classes.items():
                result[cls_name] = self.__session.query(value).all()
            return result

    def new(self, obj):
        """Adds object to storage"""
        self.__session.add(obj)

    def save(self):
        """Saves storage objects to database"""
        self.__session.commit()

    def update_snippet(self, snippet_id, title=None, code=None, desc=None):
        """Updates snippet object in storage"""
        snippet = self.get_snippet_by_snippet_id(snippet_id)
        if snippet:
            if title is not None:
                snippet.title = title
            if code is not None:
                snippet.code = code
            if desc is not None:
                snippet.description = desc
            self.save()
            return snippet

        return None

    def delete(self, obj=None):
        """Deletes object from storage"""
        if obj:
            self.__session.delete(obj)

    def delete_all(self, obj):
        """Deletes all objects from storage"""
        self.__session.query(obj).delete()
        self.save()

    def reload(self):
        """Creates all tables in database"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """Closes storage"""
        self.__session.close()

    def get_user_by_user_id(self, user_id):
        """Returns User object from database based on id"""
        return self.__session.query(User).filter_by(user_id=user_id).first()

    def get_user_by_username(self, username):
        """Returns User object from database based on username"""
        return self.__session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email):
        """Returns User object from database based on email"""
        return self.__session.query(User).filter_by(email=email).first()

    def get_snippet_by_snippet_id(self, snippet_id):
        """Returns Snippet object from database based on snippet_id"""
        return self.__session.query(Snippet).filter(
            Snippet.snippet_id == snippet_id).first()

    def get_snippets_by_user_id(self, user_id):
        """Get all snippets belonging to a user by user_id"""
        return self.__session.query(Snippet).filter(
            Snippet.user_id == user_id).all()

    def count_snippets_by_user_id(self, user_id):
        """Get number of snippets belonging to a user by user_id"""
        return self.__session.query(Snippet).filter(
            Snippet.user_id == user_id).count()

    def count_snippets(self):
        """Returns number of Snippet objects in storage"""
        return self.__session.query(Snippet).count()

    def count_users(self):
        """Returns number of User objects in storage"""
        return self.__session.query(User).count()

    def delete_user_and_snippets(self, user_id):
        """Delete all snippets belonging to a user by user_id"""
        try:
            user = self.get_user_by_user_id(user_id)
            if user:
                self.__session.query(Snippet).filter(
                    Snippet.user_id == user_id).delete(
                        synchronize_session='fetch')
                self.delete(user)
                self.save()
            else:
                raise ValueError('User not found.')
        except SQLAlchemyError as e:
            self.__session.rollback()
            # Log the error or handle it as needed
            logging.error(f"SQLAlchemyError occurred: {e}", exc_info=True)
            raise e
        finally:
            self.close()
