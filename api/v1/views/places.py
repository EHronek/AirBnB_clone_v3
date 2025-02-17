#!/usr/bin/python3
"""RESTful API actions for Place"""
from flask import request, abort, jsonify
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Gets all Place objects in a specific City"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        return jsonify({"error": "Not found"}), 404
    places = [place.to_dict() for place in city_obj.places]
    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Gets a place object by specified id in params"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place in a City"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404

    place_data = request.get_json(silent=True)
    if not place_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in place_data:
        abort(400, description="Missing user_id")
    
    user = storage.get(User, place_data['user_id'])
    if not user:
        return jsonify({"error": "Not found"}), 404

    if 'name' not in place_data:
        abort(400, description="Missing name")

    new_place = Place(city_id=city_id, **place_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404

    place_data = request.get_json(silent=True)
    if not place_data:
        abort(400, description="Not a JSON")

    keys_to_ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in place_data.items():
        if key not in keys_to_ignore:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
