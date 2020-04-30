#!/usr/bin/python3
""" Module that handles all default RestFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ list of all State objects"""
    all_states = []
    for value in storage.all("State").values():
        all_states.append(value.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """ State object with id """
    st = (storage.get('State', state_id))
    if st:
        return jsonify(st.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ that delete a State object"""
    st = storage.get('State', state_id)
    if st:
        storage.delete(st)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ That create a State object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    req_st = State(**request.get_json())
    req_st.save()
    return jsonify(req_st.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ that updates a State object """
    keys = ['id', 'created_at', 'updated_at']
    st = storage.get('State', state_id)
    if st is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key in keys:
            pass
        else:
            setattr(st, key, value)
    st.save()
    return jsonify(st.to_dict()), 200
