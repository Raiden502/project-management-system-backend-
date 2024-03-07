from flask import jsonify, request, Blueprint
from handlers.teams.team_list import TeamList
from handlers.teams.team_details import TeamDetails
from handlers.teams.team_contact_list import UserTeamList
from handlers.teams.team_create import TeamCreate
from handlers.teams.team_edit import EditTeams
from handlers.teams.team_formdata import TeamEditDetails
from handlers.teams.teams_delete import DeleteTeams
from middleware.token_middleware import token_required

team_blueprint = Blueprint("team_blueprint", __name__)

@team_blueprint.route("/team_list", methods=["POST"])
@token_required
def get_user_list(current_app):
    response = TeamList(request).get_team_list()
    return jsonify(response)

@team_blueprint.route("/team_details", methods=["POST"])
@token_required
def get_team_details(current_app):
    response = TeamDetails(request).get_team_details()
    return jsonify(response)

@team_blueprint.route("/team_contacts", methods=["POST"])
@token_required
def get_team_contacts(current_app):
    response = UserTeamList(request).get_list()
    return jsonify(response)

@team_blueprint.route("/team_create", methods=["POST"])
@token_required
def team_create(current_app):
    response = TeamCreate(request).addNewTeam()
    return jsonify(response)

@team_blueprint.route("/team_edit", methods=["POST"])
@token_required
def team_edit(current_app):
    response = EditTeams(request).editNewTeam()
    return jsonify(response)


@team_blueprint.route("/team_formdetails", methods=["POST"])
@token_required
def team_formdetails(current_app):
    response = TeamEditDetails(request).get_form_details()
    return jsonify(response)

@team_blueprint.route("/team_delete", methods=["POST"])
@token_required
def team_delete(current_app):
    response = DeleteTeams(request).delete()
    return jsonify(response)