#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """
        Represents a Review class for a MySQL database.
        Inherits from SQLAlchemy Base

        Attributes:
            __tablename__ (str): The name of the MySQL table to store Users.

            place_id (sqlalchemy String): The id of the Place.
            user_id (sqlalchemy String): The user's id.
            text (sqlalchemy String): The review.

    """
    __tablename__ = 'reviews'

    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    text = Column(String(1024), nullable=False)
