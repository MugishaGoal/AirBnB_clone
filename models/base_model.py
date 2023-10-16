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
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.strptime(value, time_format))
                    else:
                        setattr(self, key, value)
                else:
                    self.id = str(uuid.uuid4())
                    self.created_at = self.updated_at = datetime.now()
                    storage.new(self)

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.
        - The dictionary contains all instance attributes.
        - A '__class__' key is added to indicate the class name.
        - 'created_at' and 'updated_at' are represented
        as ISO-formatted strings.
        """
        class_name = self.__class__.__name__
        return {
            "__class__": class_name,
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __str__(self):
        """Returns a string representation of the object."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
