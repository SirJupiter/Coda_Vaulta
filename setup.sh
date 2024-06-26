#!/bin/bash
sudo apt-get update
sudo apt-get install python-dev python-pip # python development libraries and pip Python package manager

# Install the required Python packages
sudo pip install -r requirements.txt

# Set up database
cat database/db_setup.sql | mysql -u root -p
