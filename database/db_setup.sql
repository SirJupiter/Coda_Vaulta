-- prepares a MySQL database and user for the project

DROP DATABASE IF EXISTS codavaulta_db;

-- create database
CREATE DATABASE IF NOT EXISTS codavaulta_db;

-- create user
CREATE USER IF NOT EXISTS 'codavaulta_user'@'localhost' IDENTIFIED BY 'codavaulta_password';
GRANT ALL PRIVILEGES ON codavaulta_db.* TO 'codavaulta_user'@'localhost';

FLUSH PRIVILEGES;
