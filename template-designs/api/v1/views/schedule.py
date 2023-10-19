#!/usr/bin/python3
"""
file: service.py
Desc: Responsible for end points related to services
Authors: kidus kinde, Mulugeta Tadege, and Teklemariam Mossie
Date Created: sep 14 2022
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.schedule import Schedule


@app_views.route('/schedule', methods=['GET', "POST"])
def schedule_without_id():
    """Handles http request for services route without id"""
    if request.method == 'GET':
        # Retrives all Service objects.
        schedule = storage.all(Schedule).values()
        schedule_list = [s.to_dict() for s in schedules]
        return jsonify(schedule_list), 200

    if request.method == 'POST':
        # Creates a new Service object. name is required
        data = request.get_json()
        if data is None:
            abort(400, "Not a Json")
        if data.get("name") is None:
            abort(400, "Missing name")
        obj = Schedule(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/schedules/<schedule_id>', methods=['GET', 'DELETE', 'PUT'])
def service_with_id(schedule_id=None):
    """Handles http request for services route with id"""
    obj = storage.get(Schedule, schedule_id)
    if obj is None:
        abort(404, "Not found")
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
