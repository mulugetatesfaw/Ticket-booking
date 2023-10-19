#!/usr/bin/python3
"""
file: cities.py
Desc: Responsible for end points related to cities
Authors: Teklemariam Mossie, Mulugeta Tadege, and Kidus Kinde
Date Created: Dec 14 2022
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.bus import Bus
from models.route import Route


@app_views.route('/routes/<route_id>/buses
        ', methods=['GET', "POST"])
def bus_without_idi(route_idy=None):
    """Handles http"""
        # Retrives all City objects.
        route = storage.get(Route,route_id)
        if route is None:
            abort(400)

    if request.method == 'GET':
        # Creates a new city object. Name is a required filled.
        objs = storage.all(Bus)
        obj_list = [obj.to_dict() for obj in objs.values()
                if obj.route_id == route_id]
        return jsonify(obj_list), 200
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(400, "Not a Json")
        if data.get("name") is None:
            abort(400, "Missing name")
        if data.get("plate_no") is None:
            abort(400, "Missing plate_no")
        obj = Bus(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/buses/<bus_id>', methods=['GET', 'DELETE', 'PUT'])
def bus_with_id(bus_id=None):
    """Handles http request for buses route with id"""
    obj = storage.get(Bus, bus_id)
    if obj is None:
        abort(404, "Not found")
    if request.method == 'GET':
        # Retrives a bus object based on the bus_id.
        return jsonify(obj.to_dict())

    if request.method == 'DELETE':
        # Deletes a bus object based on the bus_id.
        obj.delete()
        del obj
        return jsonify({}), 200

    if request.method == 'PUT':
        # Updates a bus object based on the bus_id.
        data = request.get_json()
        if data is None:
            abort(400)
        IGNORE = ['id', 'created_at', 'updated_at', 'route_id']
        d = {k: v for k, v in data.items() if k not in IGNORE}
        for k, v in d.items():
            setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
