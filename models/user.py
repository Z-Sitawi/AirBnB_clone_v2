#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    Represents a User for a MySQL database.
    Inherits from SQLAlchemy Base

        Attributes:
            __tablename__ (str): The name of the MySQL table to store Users.

            email (sqlalchemy String): The email of the User.
            password (sqlalchemy String): The password of the User.
            first_name (sqlalchemy String): The first name of the User.
            last_name (sqlalchemy String): The last name of the User.

    """
    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    place = relationship('Place', backref='user', cascade="delete")