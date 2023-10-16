#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from os import path
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


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
        return FileStorage.__objects

    def new(self, obj):
        """
        Takes an object obj, gets the name of its class, and uses that along
        with the object's id to create a unique key.
        """
        ocl_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocl_name, obj.id)] = obj

    def save(self):
        """
        Serializes and saves instances from memory to the JSON file.
        """
        o_dict = FileStorage.__objects
        obj_dict = {obj: o_dict[obj].to_dict() for obj in o_dict.keys()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes and reloads instances from the JSON file into memory.

        If the JSON file exists, it reads the data and creates instances.
        """
        with open(FileStorage.__file_path) as file:
            obj_dict = json.load(file)
            for ob in obj_dict.values():
                class_name = ob["__class__"]
                del ob["__class__"]
                self.new(eval(class_name)(**ob))

        except FileNotFoundError:
            return
