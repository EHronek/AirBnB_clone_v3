#!/usr/bin/python3

from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Gets all city objects of a given State"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not Found"}), 404
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_obj(city_id):
    """Gets a City object by its city Id"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_obj(city_id):
    """Deletes a specifiec City depending on its id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City object under provided State with state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error", "Missing name"}), 400
    new_city =  City(state_id=state_id, **data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a specific City object by its ID"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    new_data = request.get_json()
    if not new_data:
        return jsonify({"error", "Not a JSON"}, 400)
    for key, value in new_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)

    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
