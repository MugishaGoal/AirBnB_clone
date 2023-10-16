#!/usr/bin/python3
"""A class that defines common attributes and methods for other classes."""
import models
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel.

        Args:
            *args: Unused.
            **kwargs: Keyword arguments representing attributes and values.
        """
        time_fmt = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.strptime(value, time_fmt))
                    else:
                        setattr(self, key, value)
        if 'id' not in kwargs:
            self.id = str(uuid4())
        if 'created_at' not in kwargs:
            self.created_at = self.updated_at = datetime.now()
        models.storage.new(self)

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.
        - The dictionary contains all instance attributes.
        - A '__class__' key is added to indicate the class name.
        - 'created_at' and 'updated_at' are represented
        as ISO-formatted strings.
        """
        rtrn_dict = self.__dict__.copy()
        rtrn_dict["created_at"] = self.created_at.isoformat()
        rtrn_dict["updated_at"] = self.updated_at.isoformat()
        rtrn_dict["__class__"] = self.__class__.__name__
        return rtrn_dict

    def __str__(self):
        """Returns a string representation of the object."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
