#!/usr/bin/python3
"""RESTful API actions on Review"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves a list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object"""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review_obj.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        return jsonify({"error": "Not found"}), 404
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    review_data = request.get_json(silent=True)
    if not review_data:
        abort(400, description="Not a JSON")
    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")

    user = storage.get(User, review_data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404
    if 'text' not in review_data:
        abort(400, description="Missing text")

    new_review = Review(place_id=place_id, **review_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a review object by id"""
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    new_data = request.json(silent=True)
    if not new_data:
        abort(400, description="Not a JSON")
    ignore_keys = ["id", "user_id", "created_at", "updated_at"]
    for key, value in new_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
