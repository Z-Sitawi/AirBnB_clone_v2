#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
        Represents a state for a MySQL database.

        Inherits from SQLAlchemy Base and links to the MySQL table states.

        Attributes:
            __tablename__ (str): The name of the MySQL table to store States.
            name (sqlalchemy String): The name of the State.
            cities (sqlalchemy relationship): The State-City relationship.
        """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get a list of all related City objects."""
            from models import storage
            city_list = []
            for city in list(storage.all("City").values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
