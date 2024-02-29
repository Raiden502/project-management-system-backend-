from flask import jsonify, request, Blueprint
from handlers.auth.registration import Registration
from handlers.auth.login import Login
from handlers.auth.authenticate import Authenticate
from middleware.token_middleware import token_required

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def handle_login_user():
    response = Login(request).getuser()
    return jsonify(response)

@auth_blueprint.route("/registration", methods=["POST"])
def handle_registration():
    response = Registration(request).addNewUser()
    return jsonify(response)

@auth_blueprint.route("/authenticate", methods=["GET"])
@token_required
def handle_auth_token(current_app):
    response = Authenticate(current_app).validate_token()
    return jsonify(response)