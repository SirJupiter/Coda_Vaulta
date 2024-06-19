#!/bin/bash
sudo apt-get update

if sudo pip install uwsgi -qq; then
	echo -e "\n	----	uwsgi successfully installed	----	\n"
else
	echo -e "\n	----	uwsgi installation failed	----	\n"
	exit 1
fi
uwsgi --version

sudo pip install bcrypt #  for hashing password passed in by user