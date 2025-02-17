#!/usr/bin/python3
"""Flask app"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.route('/api/v1/nop', strict_slashes=False)
def error_404():
    """Handles 404 errors Returns a json formatted 404 status code"""
    return jsonify({"error": "Not Found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the current db session"""

    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
