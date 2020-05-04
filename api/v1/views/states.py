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
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):

    data = storage.all("State")
    obj = 'State' + '.' + state_id

    if state_id == '1':
        new_list = []
        for v in data.values():
            new_list.append(v.to_dict())
        return jsonify(new_list)

    elif obj not in data.keys():
        return abort(404)

    else:
        for key, val in data.items():
            if obj in key:
                return jsonify(val.to_dict())
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """ that delete a State object"""
    data = storage.all('State')
    obj = 'State' + '.' + state_id
    if obj in data:
        storage.delete(data[obj])
        storage.save()
        return (jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ That create a State object"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    req_state = State(**request.get_json())
    req_state.save()
    return jsonify(req_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ that updates a State object """
    try:
        data = request.get_json()
    except:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if data is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    sts = storage.all('State')
    obj = 'State' + '.' + state_id
    if obj in sts:
        for key, val in data.items():
            if key != 'id' or key != 'created_at' or key != 'updated_at':
                setattr(sts[obj], key, val)
        storage.save()
        return (jsonify(sts[obj].to_dict()), 200)
    else:
        return abort(404)
