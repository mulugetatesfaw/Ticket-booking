#!/usr/bin/python3
"""
file: hospital_service.py
Desc: Responsible for end points related to hospital_service linkage
Authors: Gizachew Bayness, Joseph Tapano, and Helina Gebreyes
Date Created: Dec 15 2022
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.service import Service
from models.hospital import Hospital


@app_views.route('/hospitals/<hospital_id>/services', methods=['GET', 'Post'])
def multiple_services_per_hospital(hospital_id):
    """Handles HTTP requests for multiple services linked to a hospital"""
    hospital = storage.get(Hospital, hospital_id)
    if not hospital:
        abort(404)
    if request.method == "GET":
        # Retrives all Service objects linked to a Hospital object based on the
        # hospital_id.
        services = [service.to_dict() for service in hospital.services]
        return jsonify(services), 200
    if request.method == "POST":
        # Links all Service objects to a Hospital object based on the hospital_id.
        data = request.get_json()
        if data is None:
            abort(400, "Not a Json")
        service_ids = data.get("service_ids")
        if service_ids is None:
            abort(400, "Missing service_ids")
        services = []
        for service_id in service_ids:
            services.append(storage.get(Service, service_id))
        if services:
            services_to_be_added = [
                s for s in services if s not in hospital.services]
            [hospital.services.append(s) for s in services_to_be_added]
        storage.save()
        return jsonify({"number_of_new_services_added": len(services_to_be_added)})


@app_views.route('/hospitals/<hospital_id>/services/<service_id>', methods=['POST', 'DELETE'])
def single_service_per_hospital(hospital_id, service_id):
    """Handles HTTP requests for a service linked to a hospital"""
    hospital = storage.get(Hospital, hospital_id)
    service = storage.get(Service, service_id)
    if not hospital or not service:
        abort(404)
    if request.method == "POST":
        # Link a Service object to a Hospital object  based on the service_id
        # and hospital_id
        if service in hospital.services:
            return jsonify(service.to_dict()), 200
        else:
            hospital.services.append(service)
    if request.method == "DELETE":
        # Deletes a Service object to a Hospital object
        if service not in hospital.services:
            abort(404)
        hospital.services.remove(service)
    storage.save()
    return jsonify(service.to_dict()), 200
