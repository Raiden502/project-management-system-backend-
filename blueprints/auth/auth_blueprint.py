from flask import jsonify, request,Blueprint

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def handle_login_user():
    response = {"msg":"hi"}
    return jsonify(response)

@auth_blueprint.route("/registration", methods=["POST"])
def handle_registration():
    response = {"msg":"hi"}
    return jsonify(response)
