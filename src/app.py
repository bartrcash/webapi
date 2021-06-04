# dotenv
from dotenv import load_dotenv
from flask import request
from flask.helpers import make_response
import werkzeug
from os.path import join, dirname

# load env vars
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


# flask
import traceback
from flask import Flask, json

# flask migrate
from flask_migrate import Migrate

# # # # # # # # # # remove

# flask_cors
from flask_cors import CORS

# flask_jwt_extended
from flask_jwt_extended import JWTManager

# os
import os

# Modules
from modules.user import user_module

# exceptions
from errors.custom_error import CustomException

# db
from db import db


# create flask app
app = Flask(__name__)

# Add modules
app.register_blueprint(user_module, url_prefix="/api/users")

# CORS
CORS(app,supports_credentials=True)


# test routes
@app.route("/test")
def ping():
    return {"message": "welcome"}, 200


@app.route("/testmessage")
def testmessage():
    message = os.environ.get("TEST_MESSAGE")
    return {"message": message}, 200


@app.route("/setcookie")
def setcookie():
    resp = make_response({"message":"cookie saved"})
    resp.set_cookie("test","value")

    return resp


@app.route("/getcookie")
def getcookie():
    cookie = request.cookies.get("test")
    return {"cookie": cookie}, 200


@app.route("/deletecookie")
def deletecookie():
    resp = make_response({"message":"cookie saved"})
    resp.set_cookie("test","value")

    return resp



# add custom exceptions
@app.errorhandler(Exception)
def handle_custom_error(error):

    if isinstance(error, CustomException):

        response = {}
        response["message"] = error.get_message()
        return response, error.status_code

    if isinstance(error, werkzeug.exceptions.HTTPException):
        response = error.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": error.code,
                "name": error.name,
                "message": error.description,
            }
        )
        response.content_type = "application/json"
        return response, error.code

    print(str(error))
    traceback.print_exc()

    return {"message": "Error"}, 500


# Config
app.config.from_object("config")

# jwt
jwt = JWTManager(app)

# database
db.init_app(app)

# migrate
migrate = Migrate(app, db)

# run
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
