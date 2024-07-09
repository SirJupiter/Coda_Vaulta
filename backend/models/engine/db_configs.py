#!/usr/bin/python3
"""This module loads credentials for accessing database from a .env file"""

from dotenv import load_dotenv
import os

# Define the path to the .env file explicitly
dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')

# Load environment variables
load_dotenv(dotenv_path)

DB = os.getenv('DB')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
