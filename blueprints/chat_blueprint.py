from flask import jsonify, request, Blueprint
from handlers.chats.get_users import UserDetails
from handlers.chats.get_chats import UserChats
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