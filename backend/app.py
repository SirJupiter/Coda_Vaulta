#!/usr/bin/python3
"""Contains flask application that
        defines routes,
        handles requests, and
        interacts with the database
"""

from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from models.user import User
from models.snippet import Snippet
from models import storage
from datetime import timedelta
from flask_cors import CORS
from utilities import verify_password


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'codavaulta_secret_key'

# Set token expiration to 24 hours
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize JWT Manager
jwt = JWTManager(app)

CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})

# Blueprint creation
api = Blueprint('api', __name__)


@app.teardown_appcontext
def teardown(exc):
    """Closes the database session after each request"""
    storage.close()


@api.route('/user/register', methods=['POST'], strict_slashes=False)
def register_user():
    """
    Registers a new user with the provided username, email, and password.
    Expects a JSON payload with keys 'username', 'email', and 'password'.

    Returns:
        - 400 Bad Request if the user already exists or if there's a
        ValueError during user creation.
        - 201 Created on successful user creation along with user details.
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data_received = request.get_json()
    if 'username' not in data_received:
        return jsonify({"error": "Missing username"}), 400
    if 'email' not in data_received:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data_received:
        return jsonify({"error": "Missing password"}), 400

    username, email = data_received.get('username'), data_received.get('email')
    password = data_received.get('password')

    if storage.get_user_by_email(email):
        return jsonify({'error': 'User already registered'}), 400
    if storage.get_user_by_username(username):
        return jsonify({"error": "Username already exists"}), 400

    try:
        user = User(username, email, password)
        storage.new(user)
        storage.save()

        return jsonify({
            "message": "User created successfully",
            "username": user.username,
            "email": user.email
            }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api.route('/delete_user', methods=['DELETE'], strict_slashes=False)
def remove_user():
    """
    Remove a user - admin
    Expects a JSON payload with key 'user_id'.
    Returns a JSON response indicating the deletion was successful.
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data_received = request.get_json()
    if 'user_id' not in data_received:
        return jsonify({"error": "Missing user_id"}), 400

    user_id = data_received.get('user_id')

    try:
        user = storage.get_user_by_user_id(user_id)

        storage.delete(user)
        storage.save()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception:
        return jsonify({"error": "User not found"}), 400


@api.route('/user/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Logs in a user by verifying their email and password.
    Expects a JSON payload with keys 'email' and 'password'.

    Returns:
        - 400 Bad Request if the request is not JSON.
        - 401 Unauthorized if email or password is missing,
        the user is not found, or the password is invalid.
        - 200 OK on successful login along with an authentication token.
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data_received = request.get_json()
    if 'email' not in data_received:
        return jsonify({"error": "Missing email"}), 401
    if 'password' not in data_received:
        return jsonify({"error": "Missing password"}), 401

    email, password = data_received.get('email'), data_received.get('password')

    user = storage.get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not verify_password(password, user.hashed_password):
        return jsonify({"error": "Invalid password"}), 401

    access_token = create_access_token(identity=user.user_id)
    return jsonify({
        "authentication_token": access_token,
        "username": user.username.split()[0]
        }), 200


@api.route('/user/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    """
    Endpoint for logging out a user.
    Requires a valid JWT token.
    Returns a JSON response indicating the logout was successful.
    """
    user_id = get_jwt_identity()

    if storage.get_user_by_user_id(user_id):
        return jsonify({"message": "User logged out successfully"}), 200
    else:
        return jsonify({"error": "Not logged in"}), 404

    # In the future, add the token to a blacklist


@api.route('/user/delete_user', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user():
    """
    Endpoint for deleting a user.
    Requires a valid JWT token.
    Returns a JSON response indicating the deletion was successful.
    """
    user_id = get_jwt_identity()

    try:
        user = storage.get_user_by_user_id(user_id)
        if user:
            storage.delete(user)
            storage.save()
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": e}), 400


@api.route('/protected', methods=['GET'], strict_slashes=False)
@jwt_required()
def protected():
    """
    A protected endpoint that requires a valid JWT token.
    Returns the email of the logged-in user.
    """
    user_id = get_jwt_identity()
    user = storage.get_user_by_user_id(user_id)
    return jsonify(logged_in_as=user.email), 200


@api.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Endpoint to retrieve all users.
    Returns a JSON list of all users.
    """
    all_users = storage.all('User')
    if all_users:
        users = [user.to_dict() for user in all_users]
        return jsonify(users), 200
    else:
        return jsonify({"error": "No user found"}), 200


@api.route('/snippets', methods=['GET'], strict_slashes=False)
def get_all_snippets():
    """
    Endpoint to retrieve all snippets.
    Returns a JSON list of all snippets.
    """
    all_snippets = storage.all('Snippet')
    if all_snippets:
        snippets = [snippet.to_dict() for snippet in all_snippets]
        return jsonify(snippets), 200
    else:
        return jsonify({"error": "No snippet found"}), 200


@api.route('/user/create_snippet', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_user_snippet():
    """
    Endpoint for creating a new snippet.
    Requires a valid JWT token.
    Expects a JSON payload with 'title', 'code', and optionally 'description'.
    Returns a JSON response with details of the created snippet.
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data_received = request.get_json()
    if 'title' not in data_received:
        return jsonify({"error": "Missing title"}), 400
    if 'code' not in data_received:
        return jsonify({"error": "Missing code"}), 400

    if 'description' not in data_received:
        description = ''
    else:
        description = data_received.get('description')
    title, code = data_received.get('title'), data_received.get('code')

    user_id = get_jwt_identity()

    try:
        snippet = Snippet(title, code, description, user_id)
        storage.new(snippet)
        storage.save()

        return jsonify({
            "message": "Snippet created successfully",
            "snippet_id": snippet.snippet_id,
            "title": snippet.title,
            "code": snippet.code,
            "description": snippet.description
            }), 201
    except Exception as e:
        return jsonify({"error": e}), 400

    # In the future, return an html page with 'you are not logged in'
    # include a link to serve the landing page for user to login


@api.route('/user/get_snippets', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user_snippets():
    """
    Endpoint to retrieve all snippets for the logged-in user.
    Requires a valid JWT token.
    Returns a JSON list of snippets belonging to the user.
    """
    user_id = get_jwt_identity()
    snippets = storage.get_snippets_by_user_id(user_id)
    if snippets:
        snippets = [snippet.to_dict() for snippet in snippets]
        return jsonify(snippets), 200
    else:
        return jsonify({"error": "No snippet found"}), 200


@api.route('/user/update_snippet', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user_snippet():
    """
    Endpoint to update an existing snippet.
    Requires a valid JWT token.
    Expects a JSON payload with 'snippet_id' and any of 'title', 'code',
    'description' to update.
    Returns a JSON response with details of the updated snippet.
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data_received = request.get_json()
    if 'snippet_id' not in data_received:
        return jsonify({"error": "Missing snippet_id"}), 400

    snippet_id = data_received.get('snippet_id')

    user_id = get_jwt_identity()

    try:
        user = storage.get_user_by_user_id(user_id)

        snippet = storage.get_snippet_by_snippet_id(snippet_id)

        if snippet:
            if snippet.user_id == user.user_id:
                if 'title' in data_received:
                    snippet.title = data_received.get('title')
                if 'code' in data_received:
                    snippet.code = data_received.get('code')
                if 'description' in data_received:
                    snippet.description = data_received.get('description')
                snippet.updated_at = datetime.now()

                storage.save()

                return jsonify({
                    "message": "Snippet updated successfully",
                    "snippet_id": snippet.snippet_id,
                    "title": snippet.title,
                    "code": snippet.code,
                    "description": snippet.description,
                    "updated_at": snippet.updated_at.isoformat()
                    }), 200
            else:
                return jsonify({"error": "Not logged in"}), 404
        else:
            return jsonify({"error": "Snippet not found"}), 404

    except Exception as e:
        return jsonify({"error": e}), 400


@api.route('/user/delete_snippet', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user_snippet():
    """
    Endpoint to delete a snippet.
    Requires a valid JWT token.
    Expects a JSON payload with 'snippet_id'.
    Returns a JSON response indicating the deletion was successful.
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data_received = request.get_json()
    if 'snippet_id' not in data_received:
        return jsonify({"error": "Missing snippet_id"}), 400

    snippet_id = data_received.get('snippet_id')

    user_id = get_jwt_identity()

    try:
        user = storage.get_user_by_user_id(user_id)

        snippet = storage.get_snippet_by_snippet_id(snippet_id)
        if snippet and snippet.user_id == user.user_id:
            storage.delete(snippet)
            storage.save()
            return jsonify({"message": "Snippet deleted successfully"}), 200
        else:
            return jsonify({"error": "Snippet not found"}), 404
    except Exception as e:
        return jsonify({"error": e}), 400


# Blueprint registration
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)