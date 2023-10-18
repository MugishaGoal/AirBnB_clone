#!/usr/bin/python3
"""
Unit tests are provided for the 'file_storage.py' module in the 'engine'
package of the 'models' module.

Test Methods:

test_file_storage_instantiation_no_args: Tests the instantiation of
'FileStorage' without any arguments.
test_file_storage_instantiation_with_arg: Tests the instantiation of
'FileStorage' with invalid arguments.
test_file_storage_file_path_is_private_str: Tests if the '__file_path'
attribute of 'FileStorage' is a private string attribute.
test_file_storage_objects_is_private_dict: Tests if the '__objects' attribute
of 'FileStorage' is a private dictionary attribute.
test_storage_initializes: Tests if the 'models.storage' instance is correctly
initialized with the 'FileStorage' class.
"""

import os
import json
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    def test_file_storage_instantiation_no_args(self):
        storage = FileStorage()
        self.assertIsInstance(storage, FileStorage)

    def test_file_storage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_is_private_str(self):
        storage = FileStorage()
        self.assertIsInstance(storage._FileStorage__file_path, str)

    def test_objects_is_private_dict(self):
        storage = FileStorage()
        self.assertIsInstance(storage._FileStorage__objects, dict)

    def test_storage_initializes(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        all_objects = models.storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        storage = FileStorage()
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()

        storage.new(bm)
        storage.new(us)
        storage.new(st)
        storage.new(pl)
        storage.new(cy)
        storage.new(am)
        storage.new(rv)

        self.assertIn("BaseModel." + bm.id, storage.all())
        self.assertIn(bm, storage.all().values())
        self.assertIn("User." + us.id, storage.all())
        self.assertIn(us, storage.all().values())
        self.assertIn("State." + st.id, storage.all())
        self.assertIn(st, storage.all().values())
        self.assertIn("Place." + pl.id, storage.all())
        self.assertIn(pl, storage.all().values())
        self.assertIn("City." + cy.id, storage.all())
        self.assertIn(cy, storage.all().values())
        self.assertIn("Amenity." + am.id, storage.all())
        self.assertIn(am, storage.all().values())
        self.assertIn("Review." + rv.id, storage.all())
        self.assertIn(rv, storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        storage = FileStorage()
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()

        storage.new(bm)
        storage.new(us)
        storage.new(st)
        storage.new(pl)
        storage.new(cy)
        storage.new(am)
        storage.new(rv)

        storage.save()
        save_text = ""
        with open("file.json", "r") as file:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + us.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        storage = FileStorage()
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()

        storage.new(bm)
        storage.new(us)
        storage.new(st)
        storage.new(pl)
        storage.new(cy)
        storage.new(am)
        storage.new(rv)

        storage.save()
        storage.reload()

        self.assertIn("BaseModel." + bm.id, storage.all())
        self.assertIn("User." + us.id, storage.all())
        self.assertIn("State." + st.id, storage.all())
        self.assertIn("Place." + pl.id, storage.all())
        self.assertIn("City." + cy.id, storage.all())
        self.assertIn("Amenity." + am.id, storage.all())
        self.assertIn("Review." + rv.id, storage.all())

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
