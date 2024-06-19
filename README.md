## CODA VAULTA: Effortlessly Save, Organize, and Share Your Code Snippets

**A Developer's Haven for Code Management**

Coda Vaulta is your one-stop solution for managing your code snippets efficiently.  This project aims to provide a user-friendly platform where developers can:

* **Store Code Snippets:**  Effortlessly save code snippets of any language with syntax highlighting.
* **Organize with Tags & Folders (Future):**  Categorize snippets with relevant tags and organize them using folders for a structured approach (planned for future development).
* **Seamless Sharing:** Share specific snippets with colleagues or the public via unique links for easy collaboration.
* **Focus on Coding:** Coda Vaulta streamlines your workflow, allowing you to focus on writing code instead of managing it.

**Current Stage and Roadmap**

This README outlines the project in its initial stages, focusing on the core functionalities of creating, viewing, editing, and deleting code snippets.  As development progresses, the following features are planned for future incorporation:

* **User Authentication and Accounts:** Implement secure user registration and login functionalities for managing private snippets.
* **Version Control (Future):** Allow users to track changes made to snippets and revert to previous versions if needed (planned for future development).
* **Collaboration Features (Future):**  Enable developers to collaborate on snippets in real-time or asynchronously (planned for future development).
* **Advanced Search (Future):** Implement a robust search functionality to find snippets based on keywords, tags, or code content (planned for future development).

**Technology Stack**

Coda Vaulta leverages a combination of technologies to deliver a smooth user experience:

* **Frontend:**
    * Vanilla JavaScript: Provides a lightweight and customizable foundation for the user interface.
    * HTML/CSS:  Responsible for the structure and styling of the web application.
    * Prism.js (Optional):  Integrates syntax highlighting for various programming languages to enhance code readability (planned integration).
* **Backend:**
    * Python:  A versatile and widely used language chosen for its readability and extensive library ecosystem.
    * Flask:  A lightweight web framework built on top of Python for efficient backend development.
    * MySQL (Planned):  A popular open-source relational database for storing user information and code snippets. (subject to change based on chosen solution)
* **Testing:**
    * Unit testing with pytest:  Ensures the functionality of individual code components in the backend.
    * Integration testing with Postman:  Tests API endpoints and validates their interaction with the web client.

This technology stack provides a strong foundation for building a robust and scalable application.  Future considerations may include migration to a NoSQL database  like MongoDB if data storage requirements evolve.

**Project Structure**

The project adheres to a well-organized directory structure to promote maintainability and collaboration:

```
coda_vaulta/
├── README.md         # Project documentation and instructions
├── requirements.txt  # Python dependencies for the backend
├── frontend/         # Frontend code for the web client
│   ├── index.html    # Main HTML file
│   ├── app.js         # Main JavaScript file for the application logic
│   ├── styles/        # CSS stylesheets
│   └── ...            # Other frontend assets (images, fonts, etc.)
├── backend/          # Backend code for the web server
│   ├── __init__.py    # Empty file to mark the directory as a package
│   ├── app.py          # Main Flask application file
│   ├── models.py       # Data models for database interaction
│   ├── utils.py        # Utility functions used by the backend
│   └── config.py       # Configuration settings for the application
├── tests/             # Unit and integration tests
│   ├── test_models.py  # Unit tests for data models
│   └── test_api.py     # Integration tests for API endpoints
└── data/              # Database related files (if applicable)
    └── schema.sql     # Initial database schema (if using MySQL)
```

**Contributing**

Coda Vaulta welcomes contributions from the developer community!  If you're interested in getting involved, feel free to:

* Report bugs or suggest improvements by creating issues on the project repository (to be created).
* Fork the repository (to be created) and submit pull requests with your contributions.
* Follow development progress and engage in discussions (communication channels to be defined).


# Documentation for app.py

## Overview
This Python script utilizes the Flask framework to create a web application that provides a RESTful API for user and snippet management. It supports operations such as user sign-up, login, logout, snippet creation, retrieval, update, and deletion. The application integrates JWT (JSON Web Tokens) for authentication, ensuring secure access to certain endpoints. Additionally, it employs Flask-CORS to handle Cross-Origin Resource Sharing (CORS), allowing requests from different origins.

## Dependencies
- Flask: A micro web framework written in Python for building web applications.
- Flask-JWT-Extended: An extension for Flask that adds support for JWT-based authentication.
- Flask-CORS: An extension for handling Cross-Origin Resource Sharing (CORS), making cross-origin AJAX possible.
- datetime: Standard Python module for manipulating dates and times.
- models: A custom module (not provided in this script) presumably containing the ORM (Object-Relational Mapping) models for `User` and `Snippet`.
- utilities: A custom module (not provided in this script) presumably containing utility functions such as `verify_password`.

## Configuration
- JWT Secret Key: Configured to a static value (`'codavaulta_secret_key'`). In a production environment, this should be replaced with a secure, randomly generated key.
- JWT Access Token Expiry: Set to expire 24 hours after being issued.

## Endpoints
### User Management
- `/api/user/sign_up` (POST): Allows new users to sign up by providing a username, email, and password.
- `/api/user/login` (POST): Authenticates users and returns a JWT access token.
- `/api/user/logout` (POST): Logs out a user. Note: The current implementation does not invalidate the JWT token.
- `/api/users` (GET): Retrieves a list of all users.

### Snippet Management
- `/api/snippets` (GET): Retrieves all snippets.
- `/api/user/create_snippet` (POST): Allows authenticated users to create a new snippet.
- `/api/user/get_snippets` (GET): Retrieves all snippets created by the authenticated user.
- `/api/user/update_snippet` (PUT): Allows users to update their snippets.
- `/api/user/delete_snippet` (DELETE): Allows users to delete their snippets.

### Protected Test Endpoint
- `/api/protected` (GET): A test endpoint that requires authentication. Returns the email of the authenticated user.

## Functions
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

## Security Considerations
- The JWT secret key is hardcoded, which is not recommended for production environments.
- Passwords should be stored securely (hashed and salted) in the database. The script assumes this is handled in the `User` model or elsewhere, as it uses `verify_password` for verification.
- The script does not implement token invalidation on logout, meaning the token remains valid until it expires.

## Running the Application
The application can be started by executing the script. It runs on Flask's built-in server with debugging enabled, which is suitable for development but not for production use.