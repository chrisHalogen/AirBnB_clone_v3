#!/usr/bin/python3
"""
    Flask route that returns json respone
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'])
@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'])
def amenities(amenity_id=None):
    """
        amenities route that handles http requests
    """
    all_amenities = storage.all('Amenity')
    fetch_string = "{}.{}".format('Amenity', amenity_id)
    amenity_obj = all_amenities.get(fetch_string)

    if request.method == 'GET':
        if amenity_id:
            if amenity_obj:
                return jsonify(amenity_obj.to_json())
            else:
                abort(404, 'Not found')
        else:
            all_amenities = [obj.to_json() for obj in all_amenities.values()]
            return jsonify(all_amenities)

    if request.method == 'DELETE':
        if amenity_obj:
            amenity_obj.delete()
            del amenity_obj
            return jsonify({}), 200
        abort(404, 'Not found')

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        amenities = []
        new_amenity = Amenity(name=request.json['name'])
        storage.new(new_amenity)
        storage.save()
        amenities.append(new_amenity.to_dict())
        return jsonify(amenities[0]), 201

    if request.method == 'PUT':
        req_json = request.get_json()
        if amenity_obj is None:
            abort(404, 'Not found')
        if req_json is None:
            abort(400, 'Not a JSON')
        amenity_obj.bm_update(req_json)
        return jsonify(amenity_obj.to_json()), 200
