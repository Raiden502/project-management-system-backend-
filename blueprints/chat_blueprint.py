from flask import jsonify, request, Blueprint
from handlers.chats.get_users import UserDetails
from handlers.chats.get_chats import UserChats
from handlers.chats.get_org_users import OrgUserDetails
from handlers.chats.create_group import CreateGroup
from handlers.chats.get_group_data import GroupEditDetails
from handlers.chats.edit_group import EditGroup
from middleware.token_middleware import token_required

char_blueprint = Blueprint("char_blueprint", __name__)

@char_blueprint.route("/fetch_users", methods=["POST"])
@token_required
def get_chat_user(current_app):
    response = UserDetails(request).get_details_list()
    return jsonify(response)

@char_blueprint.route("/fetch_chats", methods=["POST"])
@token_required
def get_chats(current_app):
    response = UserChats(request).get_details_list()
    return jsonify(response)

@char_blueprint.route("/get_user_list", methods=["POST"])
@token_required
def get_user_list(current_app):
    response = OrgUserDetails(request).get_details_list()
    return jsonify(response)

@char_blueprint.route("/create_group", methods=["POST"])
@token_required
def create_group(current_app):
    response = CreateGroup(request).addNewUser()
    return jsonify(response)


@char_blueprint.route("/get_group_data", methods=["POST"])
@token_required
def get_group_data(current_app):
    response = GroupEditDetails(request).get_form_details()
    return jsonify(response)



@char_blueprint.route("/edit_group", methods=["POST"])
@token_required
def edit_group(current_app):
    response = EditGroup(request).editGroup()
    return jsonify(response)