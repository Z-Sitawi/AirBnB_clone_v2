#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()


class BaseModel:
    """
    Defines the BaseModel class.

    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.save()
        else:
            instance_att = {}
            for key, val in kwargs.items():
                if key == 'updated_at':
                    instance_att['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                                   '%Y-%m-%dT%H:%M:%S.%f')
                elif key == 'created_at':
                    instance_att['created_at'] = datetime.strptime(kwargs['created_at'],
                                                                   '%Y-%m-%dT%H:%M:%S.%f')
                elif key == '__class__':
                    pass
                elif not hasattr(self, key):
                    instance_att[key] = val
            self.__dict__.update(instance_att)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            dictionary.pop('_sa_instance_state')
        return dictionary

    def delete(self):
        from models import storage
        """
        Deletes the current instance from the storage (models.storage)
        """
        storage.delete(self)
