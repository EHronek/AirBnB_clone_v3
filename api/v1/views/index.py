#!/usr/bin/python3
"""index.py"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the api"""
    return jsonify({"status":"OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    stats_data = {
        "amenities" : storage.count(Amenity),
        "places": storage.count(Place),
        "cities": storage.count(City),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats_data)
