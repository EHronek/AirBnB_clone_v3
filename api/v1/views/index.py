#!/usr/bin/python3
"""index.py"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """Returns the status of the api"""
    return jsonify({"status":"OK"})
