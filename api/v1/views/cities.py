#!/usr/bin/python3
""" handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.base_model import *
from models.state import State
from api.v1.views import app_views
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ list of all cities """
    state_exist = storage.get(State, state_id)
    if state_exist is None:
        abort(404)
    all_cities = storage.all('City')
    list_cities = []
    for city in all_cities.values():
        if city.state_id == state_id:
            list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_by_Id(city_id):
    """ retrieves one city """
    theCity = storage.all('City')
    obj = 'City' + '.' + city_id
    if obj in theCity.keys():
        return jsonify(theCity[obj].to_dict())
    return (abort(404))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """ deletes one city by id"""
    a_city = storage.get(City, city_id)
    if a_city is None:
        abort(404)
    else:
        storage.delete(a_city)
        storage.save()
        answer = {}
        return jsonify(answer)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ HTTP request to create a city """
    state_existe = storage.get(State, state_id)
    if state_existe is None:
        abort(404)
    new_city = request.get_json(silent=True)
    if new_city is None:
        return "Not a JSON", 400
    if 'name' in new_city:
        new_city['state_id'] = state_id
        city_ready = City(**new_city)
        storage.new(city_ready)
        storage.save()
        return jsonify(city_ready.to_dict()), 201
    else:
        return ("Missing name", 400)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ PUT request for updates the city objects """
    e_city = request.get_json(silent=True)
    if e_city is None:
        return "Not a JSON", 400
    city_change = storage.get(City, city_id)
    if city_change is None:
        abort(404)
    ls_ignore = ['id', 'state_id', 'updated_at', 'created_at']
    city_change.save()
    for key, value in e_city.items():
        if key not in ls_ignore:
            setattr(city_change, key, value)
    storage.save()
    return jsonify(city_change.to_dict())
