#!/usr/bin/python3
"""Create an instance of the Storage class and reload it"""

from models.engine.storage import Storage

storage = Storage()
storage.reload()
