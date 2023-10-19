#!/usr/bin/python3
"""
file: base.py
Desc: Base model which will be shared among other models
Authors: Mulugeta Tadege,Teklemariam Mossie, and Kidus Kinde
Date Created: Sep  29 2023
"""


from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """The BaseModel class for all models"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initializes the BaseModel class with preferable attributes"""
        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"],
                                                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """String representation of instances"""
        rep = "[{:s}] ({:s}) {}".format(type(self).__name__, self.id,
                                        self.__dict__)
        return rep

    def to_dict(self):
        """Dictionary representation of an instance"""
        my_dict = self.__dict__.copy()
        cls_name = type(self).__name__
        my_dict['__class__'] = cls_name
        try:
            my_dict['created_at'] = my_dict['created_at'].isoformat()
            my_dict['updated_at'] = my_dict['updated_at'].isoformat()
        except KeyError:
            pass
        if "_sa_instance_state" in my_dict:
            del my_dict["_sa_instance_state"]
        if cls_name == "User":
            del my_dict['password']
        return my_dict

    def save(self):
        """Updates the value of updated_at"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def delete(self):
        """"Deletes an instance from the database engine"""
        from models import storage
        storage.delete(self)
