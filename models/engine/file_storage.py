#!/usr/bin/env python
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from os import path


class FileStorage:
    """
    The `FileStorage` class is responsible for managing the storage
    of instances in a JSON file.

    Attributes:
        __file_path (str): The path to the JSON file for storing instances.
        __objects (dict): A dictionary to hold instances in memory.

    Methods:
        all(self): Retrieves all instances stored in memory (__objects).
        new(self, obj): Adds a new instance to the dictionary of objects.
        save(self): Serializes and saves instances from memory to the
        JSON file.
        reload(self): Deserializes and reloads instances from the JSON
        file into memory.

    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Retrieves all instances stored in memory (__objects).

        Returns:
            dict: A dictionary containing all stored instances.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds a new instance to the dictionary of objects.

        Args:
            obj (BaseModel): The instance to be added.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes and saves instances from memory to the JSON file.
        """
        data = {}
        for key, obj in self.__objects.items():
            data[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def reload(self):
        """
        Deserializes and reloads instances from the JSON file into memory.

        If the JSON file exists, it reads the data and creates instances.
        """
        if path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for key, value in data.items():
                    class_name, obj_id = key.split(".")
                    obj = models.classes[class_name](**value)
                    self.__objects[key] = obj
