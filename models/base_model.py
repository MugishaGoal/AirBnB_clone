#!/usr/bin/python3
"""A class that defines common attributes and methods for other classes."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the class BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        t_form = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
        else:
            storage.new(self)

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""
        self.updated_at = datetime.today()
        storage.save()

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
