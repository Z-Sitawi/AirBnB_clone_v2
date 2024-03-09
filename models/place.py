#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Float, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                        Column('place_id',
                               String(60), ForeignKey('places.id'),
                               nullable=False, primary_key=True),
                        Column('amenity_id',
                               String(60), ForeignKey('amenities.id'),
                               nullable=False, primary_key=True),
                        )


class Place(BaseModel, Base):
    """
    Represents a Place for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table places.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store places.

        city_id (sqlalchemy String): The place's city id.
        user_id (sqlalchemy String): The place's user id.
        name (sqlalchemy String): The name.
        description (sqlalchemy String): The description.
        number_rooms (sqlalchemy Integer): The number of rooms.
        number_bathrooms (sqlalchemy Integer): The number of bathrooms.
        max_guest (sqlalchemy Integer): The maximum number of guests.
        price_by_night (sqlalchemy Integer): The price by night.
        latitude (sqlalchemy Float): The place's latitude.
        longitude (sqlalchemy Float): The place's longitude.
        reviews (sqlalchemy relationship): The Place-Review relationship.
        amenities (sqlalchemy relationship): The Place-Amenity relationship.
        amenity_ids (list): An id list of all linked amenities.
    """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship('Review', backref='place', cascade="delete")
    amenities = relationship("Amenity", secondary='place_amenity', viewonly=False,
                             back_populates="places")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Get a list of all related review objects."""
            from models import storage
            reviews_list = []
            for review in list(storage.all("Review").values()):
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """Get a list of all related amenity objects."""
            from models import storage
            amenities_list = []
            for amenity in list(storage.all("Amenity").values()):
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, amenity_object):
            """ handles append method for adding an (Amenity.id)
                to the attribute amenity_ids
                This method accepts only Amenity object, otherwise, does nothing.
            """
            from models.amenity import Amenity
            if not isinstance(amenity_object, Amenity):
                return

            self.amenity_ids.append(amenity_object.id)
