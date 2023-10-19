#!/usr/bin/python3
"""
file: users.py
Desc: Responsible for end points related to users
Authors: Teklemariam Mossie, kidus kinde, and Mulugeta Tadege
Date Created: sep14 2022
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET', "POST"])
def user_without_id():
    """Handles http request for users route without id"""
    if request.method == 'GET':
        # Retrives all User objects.
        users = storage.all(User).values()
        users_list = [u.to_dict() for u in users]
        return jsonify(users_list), 200

    if request.method == 'POST':
        # Creates a new User object.
        # email, and password are required
        data = request.get_json()
        if data is None:
            abort(400, "Not a Json")
        if data.get("email") is None:
            abort(400, "Missing email")
        if data.get("password") is None:
            abort(400, "Missing password")
        obj = User(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_with_id(user_id=None):
    """Handles http request for users route with id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404, "Not found")
    if request.method == 'GET':
        # Retrives a User object based on the user_id.
        return jsonify(obj.to_dict())
    if request.method == 'DELETE':
        # Deletes a User object based on the user_id.
        obj.delete()
        del obj
        return jsonify({}), 200

    if request.method == 'PUT':
        # Updates a User object based on the user_id.
        data = request.get_json()
        if data is None:
            abort(400)
        IGNORE = ['id', 'created_at', 'updated_at', 'email']
        d = {k: v for k, v in data.items() if k not in IGNORE}
        for k, v in d.items():
            setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
