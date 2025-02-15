#!/usr/bin/python3
"""
RESTful api operations for states objects
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrives all state objects"""
    all_states = storage.all(State).values()
    return jsonify([state.to_dict() for state in all_states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """Retrieves a specific state object by id"""
    fetched_state = storage.get(State, state_id)
    if not fetched_state:
        return jsonify({"error": "Not found"}), 404
    return jsonify(fetched_state.to_dict())


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State"""
    request_data = request.get_json(silent=True)
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request_data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**request_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update an existing state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_data = request.get_json(silent=True)
    if not new_data:
        return jsonify({"error": "Not a JSON"})

    keys_to_ignore = {"id", "created_at", "updated_at"}
    for k, v in new_data.items():
        if k not in keys_to_ignore:
            setattr(state, k, v)

    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes an existing state from the database"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
