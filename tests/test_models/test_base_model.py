#!/usr/bin/python3
"""Defines unittests for models/base_model.py"""
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def test_creation(self):
        my_model = BaseModel()
        self.assertIsInstance(my_model, BaseModel)

    def test_string_representation(self):
        my_model = BaseModel()
        expected_str = "[BaseModel] ({}) {}".format(
                my_model.id, my_model.__dict__)
        self.assertEqual(str(my_model), expected_str)

    def test_save_method(self):
        my_model = BaseModel()
        original_updated_at = my_model.updated_at
        my_model.save()
        self.assertNotEqual(my_model.updated_at, original_updated_at)

    def test_to_dict_method(self):
        my_model = BaseModel()
        my_model_dict = my_model.to_dict()
        self.assertIsInstance(my_model_dict, dict)
        self.assertEqual(my_model_dict['__class__'], 'BaseModel')
        self.assertIn('id', my_model_dict)
        self.assertIn('created_at', my_model_dict)
        self.assertIn('updated_at', my_model_dict)


if __name__ == '__main__':
    unittest.main()
