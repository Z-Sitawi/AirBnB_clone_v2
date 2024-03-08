#!/usr/bin/python3
"""This module defines the DB Storage engine for hbnb clone"""
from models.base_model import Base
from models.city import City
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
        Represents a database storage engine.

        Attributes:
            __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
            __session (sqlalchemy.Session): The working SQLAlchemy session.
        """
    __engine = None
    __session = None

    def __init__(self):
        """ initializes a new DB storage """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        url = f"mysql+mysqldb://{user}:{passwd}@{host}/{db}"

        self.__engine = create_engine(url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Drop all tables
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        if cls is None:
            objs = (
                    self.__session.query(State).all()
                    + self.__session.query(City).all()
                    + self.__session.query(User).all()
                    + self.__session.query(Place).all()
                    + self.__session.query(Review).all()
                    + self.__session.query(Amenity).all()
            )
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls).all()

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
