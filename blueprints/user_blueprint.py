from flask import jsonify, request, Blueprint
from handlers.users.get_users import UserDetails
from handlers.users.edit_user import UserEditDetails
from handlers.users.create_user import CreateUser
from middleware.token_middleware import token_required

user_blueprint = Blueprint("user_blueprint", __name__)

@user_blueprint.route("/user_list", methods=["POST"])
@token_required
def get_user_list(current_app):
    response = UserDetails(request).get_details_list()
    return jsonify(response)


@user_blueprint.route("/user_details", methods=["POST"])
@token_required
def get_user_details(current_app):
    response = UserDetails(request).get_details()
    return jsonify(response)

@user_blueprint.route("/edit_user_details", methods=["POST"])
@token_required
def edit_user_details(current_app):
    response = UserEditDetails(request).update_details()
    return jsonify(response)

@user_blueprint.route("/create_user", methods=["POST"])
@token_required
def create_user(current_app):
    response = CreateUser(request).addNewUser()
    return jsonify(response)

@user_blueprint.route("/update_password", methods=["POST"])
def update_password():
    response = UserEditDetails(request).update_password()
    return jsonify(response)
