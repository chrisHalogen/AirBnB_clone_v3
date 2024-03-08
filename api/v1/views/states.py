#!/usr/bin/python3
"""states request handler for CRUD operations"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states(state_id=None):
    """function to handle state requests"""
    all_states = storage.all('State')
    fetch_string = "{}.{}".format('State', state_id)
    state_obj = all_states.get(fetch_string)

    if request.method == 'GET':
        if state_id:
            if state_obj:
                return jsonify(state_obj.to_json())
            else:
                abort(404, 'Not found')
        else:
            all_states = list(obj.to_json() for obj in all_states.values())
            return jsonify(all_states)

    if request.method == 'DELETE':
        if state_obj:
            state_obj.delete()
            del state_obj
            return jsonify({})
        abort(404, 'Not found')

    if request.method == 'POST':
        # req_json = request.get_json()
        # if req_json is None:
        #     abort(400, 'Not a JSON')
        # if req_json.get("name") is None:
        #     abort(400, 'Missing name')
        # State = CNC.get("State")
        # new_object = State(**req_json)
        # new_object.save()
        # return jsonify(new_object.to_json()), 201
        '''Creates a State'''
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        states = []
        new_state = State(name=request.json['name'])
        storage.new(new_state)
        storage.save()
        states.append(new_state.to_dict())
        return jsonify(states[0]), 201

    if request.method == 'PUT':
        req_json = request.get_json()
        if state_obj is None:
            abort(404, 'Not found')
        if req_json is None:
            abort(400, 'Not a JSON')
        state_obj.bm_update(req_json)
        return jsonify(state_obj.to_json())