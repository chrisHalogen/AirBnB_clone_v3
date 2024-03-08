#!/usr/bin/python3
"""Flask App with AirBnB static HTML Template"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
import os
from werkzeug.exceptions import HTTPException


# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """after each request, this method calls .close()"""
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """All exeptions handler"""
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """Custom Error Function for the app"""
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


def run_main_app():
    """run the main functionality of the app"""
    setup_global_errors()
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port)


if __name__ == "__main__":
    """main flask app"""
    run_main_app()
