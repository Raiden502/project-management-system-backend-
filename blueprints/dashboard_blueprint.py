from flask import jsonify, request, Blueprint
from handlers.dashboard.dashboard import Dashboard
from middleware.token_middleware import token_required

dash_blueprint = Blueprint("dash_blueprint", __name__)


@dash_blueprint.route("/get_counts", methods=["POST"])
@token_required
def get_counts(current_app):
    response = Dashboard(request).get_counts()
    return jsonify(response)

@dash_blueprint.route("/get_priority_counts", methods=["POST"])
@token_required
def get_priority_counts(current_app):
    response = Dashboard(request).get_priority_counts()
    return jsonify(response)

@dash_blueprint.route("/get_stage_counts", methods=["POST"])
@token_required
def get_stage_counts(current_app):
    response = Dashboard(request).get_stage_counts()
    return jsonify(response)

@dash_blueprint.route("/get_tasks_list", methods=["POST"])
@token_required
def get_tasks_list(current_app):
    response = Dashboard(request).get_tasks_list()
    return jsonify(response)

@dash_blueprint.route("/get_user_list", methods=["POST"])
@token_required
def get_user_list(current_app):
    response = Dashboard(request).get_user_lists()
    return jsonify(response)

@dash_blueprint.route("/get_timeline", methods=["POST"])
@token_required
def get_timeline(current_app):
    response = Dashboard(request).get_timeline()
    return jsonify(response)

@dash_blueprint.route("/get_performance", methods=["POST"])
@token_required
def get_performance(current_app):
    response = Dashboard(request).get_performance()
    return jsonify(response)


