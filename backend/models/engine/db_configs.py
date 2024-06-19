#!/usr/bin/python3
"""This module loads credentials for accessing database from a .env file"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB = os.getenv('DB')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
