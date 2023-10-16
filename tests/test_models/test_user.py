#!/usr/bin/python3
"""A test for User class and FileStorage"""
import unittest
from models.user import User
from models.engine.file_storage import FileStorage
import os


class TestUser(unittest.TestCase):
    def setUp(self):
        """
        Set up a `User` instance with sample data and
        ensure a clean file.
        """
        self.user = User()
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.email = "john.doe@example.com"
        self.user.password = "secure_password"

        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up and remove the `User` instance and any stored data."""
        del self.user
        del FileStorage._FileStorage__objects

    def test_serialization(self):
        """Test the serialization of a `User` instance to a dictionary."""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["last_name"], "Doe")
        self.assertEqual(user_dict["email"], "john.doe@example.com")
        self.assertEqual(user_dict["password"], "secure_password")

    def test_deserialization(self):
        """
        Test the deserialization of a `User` instance from the JSON
        data stored in the file.
        """
        user_dict = self.user.to_dict()
        user_json = FileStorage().all()
        self.assertEqual(len(user_json), 1)
        user_id = list(user_json.keys())[0]
        new_user = user_json[user_id]
        self.assertEqual(new_user["first_name"], "John")
        self.assertEqual(new_user["last_name"], "Doe")
        self.assertEqual(new_user["email"], "john.doe@example.com")
        self.assertEqual(new_user["password"], "secure_password")


if __name__ == '__main__':
    unittest.main()
