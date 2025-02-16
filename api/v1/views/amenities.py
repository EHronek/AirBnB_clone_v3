#!/usr/bin/python3
"""script that handles RESTful actions for amenities"""
from models import storage
from flask import request, jsonify, abort
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity)
    if not amenities:
        return jsonify({"error": "Not found"}), 404
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_id(amenity_id):
    """Retrieves amenity object by ID"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity_obj.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity object"""
    amenity_data = request.get_json(silent=True)
    if not amenity_data:
        abort(400, description="Not a JSON")
    if "name" not in amenity_data:
        abort(400, description="Missing name")
    new_amenity = Amenity(**amenity_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates a Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        return jsonify({"error": "Not found"}), 404

    new_data = request.get_json(silent=True)
    if not new_data:
        abort(400, description="Not a JSON")

    for key, value in new_data.items():
        if key not in ['id', 'created_at', 'update_at']:
            setattr(amenity_obj, key, value)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
