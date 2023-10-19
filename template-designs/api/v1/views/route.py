#!/usr/bin/python3
"""
file: ticket.py
Authors: Teklemariam Mossie, kidus kinde, and Mulugeta Tadege
Date Created: Sep 14 2023
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.route import Route

@app_views.route('/routes', methods=['GET', "POST"])
def route_without_id():
    """Handles http request for ticket route without id"""
    if request.method == 'GET':
        routes = storage.all(Route).values()
        routes_list = [c.to_dict() for c in routes]
        return jsonify(routes_list), 200
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            abort(404, "Not a Json")
        if data.get("name") is None:
            abort(400, "Missing name")
        obj = Route(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201



@app_views.route('/routes/<route_id>' method=['GET', 'DELETE', 'PUT'])
def route_with_id(route_id=None):
        # Retrives all Hospital objects linked to a City object based
        # on the city_id
    obj = storage.get(Route, route_id)
    if obj is None:
        abort(400, "Not found")
    if request.method == 'GET':
        return jsonify(obj.to_dict())

    if request.method == 'DELETE':
        obj.delete()
        del obj
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            abort(400)
        IGNORE = ['id', 'created_at', 'updated_at']

        d = {k: v for k, v in data.items() if k not in IGNORE}
        for k, v in d.items():
            setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200


