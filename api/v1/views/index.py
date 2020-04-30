#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ that returns status in json format """
    return jsonify({'status': "OK"})


@app_views.route('/stats', strict_slashes=False, endpoint='count')
def stats():
    """ endpoint that retrieves the number of each objects by type """
    classes = {"City": "cities",
               "Amenity": "amenities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}

    my_dict = storage.all()
    new_dict = {}
    for key, value in classes.items():
        if storage.count(key) != 0:
            new_dict[value] = storage.count(key)
    return new_dict
