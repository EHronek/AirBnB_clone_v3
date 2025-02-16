#!/usr/bin/python3
"""RESTful api actions for User"""
from models import storage
from flask import request, abort, jsonify
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Gets all User objects """
    users = storage.all(User)
    if not users:
        return jsonify({"error": "Not found"}), 404
    all_users = [user.to_dict() for user in users.values()]
    return jsonify(all_users), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Gets the user object by id"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object by id"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user """
    user_data = request.get_json(silent=True)
    if not user_data:
        abort(400, description="Not a JSON")
    if 'email' not in user_data:
        abort(400, description="Missing email")
    if 'password' not in user_data:
        abort(400, description="Missing password")

    new_user = User(**user_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates an existing user object"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    new_data = request.get_json(silent=True)
    if not new_data:
        abort(400, description="Not a JSON")
    for key, value in new_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict(), 200)
