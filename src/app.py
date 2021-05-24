# flask
from flask import Flask, jsonify

import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

# flask_cors
from flask_cors import CORS

# flask_jwt_extended
from flask_jwt_extended import JWTManager

# os
import os
from os.path import join, dirname

# dotenv
from dotenv import load_dotenv


# Modules
from modules.user import user_module

# exceptions
# from errors.custom_error import CustomException

# load env vars
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# create flask app
app = Flask(__name__)

# Add modules
app.register_blueprint(user_module, url_prefix="/api/users")

# CORS
CORS(app)


@app.route("/test")
def ping():
    return {"message": "welcome"}, 200


@app.route("/testmessage")
def pingenv():
    message = os.environ.get("TEST_MESSAGE")
    return {"message": message}, 200


# add custom exceptions
# @app.errorhandler(CustomException)
# def handle_custom_error(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response


# Config
app.config.from_object("config")
jwt = JWTManager(app)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, host='0.0.0.0')  # important to mention debug=True
