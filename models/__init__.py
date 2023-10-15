#!/usr/bin/python3
"""A link file for storage and models directory"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
