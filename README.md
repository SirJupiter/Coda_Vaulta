# CODA VAULTA: Effortlessly Save, Organize, and Share Your Code Snippets
[Coda Vaulta](https://coda-vaulta-frontend.vercel.app/)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Details](#project-details)
  - [Technology Stack](#technology-stack)
  - [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [User Management](#user-management)
  - [Snippet Management](#snippet-management)
  - [Protected Test Endpoint](#protected-test-endpoint)
- [Documentation for app.py](#documentation-for-app.py)
  - [Overview](#overview)
  - [Dependencies](#dependencies)
  - [Configuration](#configuration)
  - [Endpoints](#endpoints)
    - [User Management](#user-management)
  - [Snippet Management](#snippet-management)
  - [Protected Test Endpoint](#protected-test-endpoint)
  - [Functions](#functions)
  - [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [Future Developments](#future-developments)
- [Acknowledgements](#acknowledgements)
- [Author](#author)

## Overview

**A Developer's Haven for Code Management**

Coda Vaulta is a web application designed to help developers manage their code snippets efficiently. It offers a secure and user-friendly platform for storing, organizing, and retrieving code snippets, enhancing productivity and code reuse.

- **Store Code Snippets:** Effortlessly save code snippets of any language with syntax highlighting.
- **Organize with Tags & Folders (Future):** Categorize snippets with relevant tags and organize them using folders for a structured approach (planned for future development).
- **Seamless Sharing (Future):** Share specific snippets with colleagues or the public via unique links for easy collaboration (planned for future development).
- **Focus on Coding:** Coda Vaulta streamlines your workflow, allowing you to focus on writing code instead of managing it.

## Features

- **User Authentication**: Secure login and registration system.
- **Snippet Organization**: Categorize snippets for easy access.
- **Search Functionality**: Quickly find the snippets you need.
- **Syntax Highlighting**: Supports a wide range of programming languages.

## Project Details

### Technology Stack

Coda Vaulta leverages a combination of technologies to deliver a smooth user experience:

- **Frontend:**
  - Vanilla JavaScript: Provides a lightweight and customizable foundation for the user interface.
  - HTML/CSS: Responsible for the structure and styling of the web application.
  - Prism.js: Integrates syntax highlighting for various programming languages to enhance code readability (planned integration).
- **Backend:**
  - Python: A versatile and widely used language chosen for its readability and extensive library ecosystem.
  - Flask: A lightweight web framework built on top of Python for efficient backend development.
  - MySQL: A popular open-source relational database for storing user information and code snippets. (subject to change based on chosen solution)
- **Testing:**
  - Unit testing with unittest: Ensures the functionality of individual code components in the backend.
  - Integration testing with Postman and VScode ThunderClient: Tests API endpoints and validates their interaction with the web client.

This technology stack provides a strong foundation for building a robust and scalable application. Future considerations may include migration to a NoSQL database like MongoDB if data storage requirements evolve.

### Project Structure

The project adheres to a well-organized directory structure to promote maintainability and collaboration:

```
Coda_Vaulta/
├── README.md # Project documentation and instructions
├── backend/
│ ├── Dockerfile # Dockerfile for building the backend container
│ ├── **init**.py # Initializes Python package for the backend
│ ├── app.py # Main Flask application entry point
│ ├── console.py # Command-line interface utilities
│ ├── models/
│ │ ├── **init**.py # Initializes Python package for models
│ │ ├── base.py # Declarative base model definition from sqlalchemy.ext.declarative
│ │ ├── engine/
│ │ │ ├── **init**.py # Initializes Python package for the database engine
│ │ │ ├── db_configs.py # Database configuration settings
│ │ │ └── storage.py # Database storage engine implementation
│ │ ├── snippet.py # Snippet model definition
│ │ └── user.py # User model definition
│ ├── requirements.txt # Python dependencies for the backend
│ ├── test_database.db # SQLite database file for testing
│ ├── tests/
│ │ ├── **init**.py # Initializes Python package for tests
│ │ ├── test.env # Environment variables for testing
│ │ ├── test_console.py # Tests for console utilities
│ │ ├── test_models/
│ │ │ ├── **init**.py # Initializes Python package for model tests
│ │ │ ├── test_engine/
│ │ │ │ ├── **init**.py# Initializes Python package for engine tests
│ │ │ │ └── test_storage.py # Tests for the storage engine
│ │ │ ├── test_snippet.py# Tests for the snippet model
│ │ │ └── test_user.py # Tests for the user model
│ │ └── test_utilities.py # Tests for utility functions
│ └── utilities.py # Utility functions for the backend
├── database/
│ ├── db_setup.sql # SQL script for setting up the database
│ └── schema.sql # SQL schema definition
├── docker-compose.yml # Docker Compose configuration for local development
├── frontend/
│ ├── Dockerfile # Dockerfile for building the frontend container
│ ├── README.md # Documentation for the frontend
│ ├── assets/
│ │ ├── images/
│ │ │ └── CodaVaulta.png # Logo image
│ │ ├── scripts/
│ │ │ ├── downloadScript.js # Script for downloading snippets
│ │ │ ├── init.js # Initialization script
│ │ │ └── prism.js # Syntax highlighting script
│ │ └── styles/
│ │ ├── del-modal.css # Styles for the delete modal
│ │ ├── overlay.css # Overlay styles
│ │ ├── prism.css # Styles for syntax highlighting
│ │ ├── responsive.css # Responsive design styles
│ │ ├── snippet-cards.css # Styles for snippet cards
│ │ └── styles.css # Main stylesheet
│ ├── cd.ico # Favicon
│ └── index.html # Main HTML file for the frontend
├── nginx_config # NGINX configuration files for deployment
├── requirements.txt # Python dependencies for the entire project
├── setup.sh # Shell script for setting up the project
└── systemd_config.service # Systemd service file for deployment

```

## API Endpoints

### User Management

- **Sign Up**: `/api/user/sign_up` (POST)
- **Login**: `/api/user/login` (POST)
- **Logout**: `/api/user/logout` (POST)
- **List Users**: `/api/users` (GET)

### Snippet Management

- **List Snippets**: `/api/snippets` (GET)
- **Create Snippet**: `/api/user/create_snippet` (POST)
- **Get User Snippets**: `/api/user/get_snippets` (GET)
- **Update Snippet**: `/api/user/update_snippet` (PUT)
- **Delete Snippet**: `/api/user/delete_snippet` (DELETE)

### Protected Test Endpoint

- **Test Authentication**: `/api/protected` (GET)

## Documentation for app.py

### Overview

This Python script utilizes the Flask framework to create a web application that provides a RESTful API for user and snippet management. It supports operations such as user sign-up, login, logout, snippet creation, retrieval, update, and deletion. The application integrates JWT (JSON Web Tokens) for authentication, ensuring secure access to certain endpoints. Additionally, it employs Flask-CORS to handle Cross-Origin Resource Sharing (CORS), allowing requests from different origins.

### Dependencies

- **Flask:** A micro web framework written in Python for building web applications.
- **Flask-JWT-Extended:** An extension for Flask that adds support for JWT-based authentication.
- **Flask-CORS:** An extension for handling Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible.
- **datetime:** Standard Python module for manipulating dates and times.
- **models:** A custom module containing the ORM (Object-Relational Mapping) models for `User` and `Snippet` inside [user.py](../Coda_Vaulta/backend/models/user.py) and [snippet.py](../Coda_Vaulta/backend/models/snippet.py).
- **utilities:** A custom module, from [utilities.py](../Coda_Vaulta/backend/utilities.py), containing utility functions such as `verify_password`.

### Configuration

- **JWT Secret Key:** Configured in a private .env file for security purposes.
- **JWT Access Token Expiry:** Set to expire 24 hours after being issued.

### Endpoints

- #### User Management

	- `/api/user/sign_up` (POST): Allows new users to sign up by providing a username, email, and password.
	- `/api/user/login` (POST): Authenticates users and returns a JWT access token.
	- `/api/user/logout` (POST): Logs out a user. Note: The current implementation does not invalidate the JWT token.
	- `/api/users` (GET): Retrieves a list of all users.

- #### Snippet Management

	- `/api/snippets` (GET): Retrieves all snippets.
	- `/api/user/create_snippet` (POST): Allows authenticated users to create a new snippet.
	- `/api/user/get_snippets` (GET): Retrieves all snippets created by the authenticated user.
	- `/api/user/update_snippet` (PUT): Allows users to update their snippets.
	- `/api/user/delete_snippet` (DELETE): Allows users to delete their snippets.

- #### Protected Test Endpoint

	- `/api/protected` (GET): A test endpoint that requires authentication. Returns the email of the authenticated user.

### Functions

- `teardown`: Closes the database session after each request.
- `create_user`: Handles user creation.
- `login`: Authenticates users and issues JWT tokens.
- `logout`: Placeholder for logging out users.
- `protected`: Test endpoint for authenticated access.
- `get_all_users`: Retrieves all user records.
- `get_all_snippets`: Retrieves all snippet records.
- `create_snippet`: Handles snippet creation for authenticated users.
- `get_user_snippets`: Retrieves snippets created by the authenticated user.
- `update_user_snippet`: Allows users to update their snippets.
- `delete_user_snippet`: Allows users to delete their snippets.

### Security Considerations

- The JWT secret key is stored in a private .env file, which is recommended for production environments.
- Passwords are stored securely (hashed and salted) in the database. This is handled in the `User` model, as it uses `verify_password` for verification.
- The script does not implement token invalidation on logout, meaning the token remains valid until it expires.

## Contributing

Coda Vaulta welcomes contributions from the developer community! If you're interested in getting involved, feel free to:

- Report bugs or suggest improvements by creating issues on the project repository (to be created).
- Fork the repository (to be created) and submit pull requests with your contributions.
- Follow development progress and engage in discussions (communication channels to be defined).

## Future Developments

- **Version Control (Future):** Allow users to track changes made to snippets and revert to previous versions if needed.
- **Collaboration Features (Future):** Enable developers to collaborate on snippets in real-time or asynchronously.
- **Advanced Search (Future):** Implement a robust search functionality to find snippets based on keywords, tags, or code content.

## Acknowledgements

- All contributors who have helped improve Coda Vaulta.
- ALX Software Engineering fellows who showed support and contributed in the form of advices on architecture, codes, and implementations of various forms.
- ALX Software Engineering Cohorts 20 and 1-Blended peers.

## Author
👤  ### Tobiloba Adeleke
- GitHub: [SirJupiter](https://github.com/SirJupiter)

Tobiloba is a backend software engineer, learning on the ALX Software Engineering program as at when Coda Vaulta was created _(July 2024)_ as a portfolio project for the conclusion of the foundations phase. He is versed in the frontend arena, making use of JavaScript and some basic React in getting the app UI done at the present level of his training. He worked on the system design, database and REST API for the Coda Vaulta project. His knowledge in both front end and back end makes it possible for him to integrate both sides of the app and understand how they work together.
His aim is to become a full-fledged full stack software engineer in the not-so-distant future.

- Email: [jupitertoby@gmail.com](mailto:jupitertoby@gmail.com)
- Project Link: [https://github.com/SirJupiter/Coda_Vaulta](https://github.com/SirJupiter/Coda_Vaulta)
