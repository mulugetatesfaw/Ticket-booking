#!/usr/bin/python3
"""
file: app.py
Desc: A module to initiate the API
Authors: Teklemariam Mossie, Mulugeta Tadege, and Kidus Kinde
Date Created: Sep 14 2022
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    d = error.description
    msgs = ["Missing name", "Missing email",
            "Missing password", "Missing user_id",
            "Missing text"]
    message = 'Not a Json' if d not in msgs else d
    return make_response(jsonify({'error': message}), 400)

@app.teardown_appcontext
def tear_down_db(execute):
    """Removes the current SQLAlchemy session after each request
    is completed"""
    storage.close()
if __name__ == "__main__":
    app.run(host=getenv('GUZO_API_ADDRESS', '0.0.0.0'),
            port=getenv('GUZO_API_PORT ', 5000),
            threaded=True, debug=True)
