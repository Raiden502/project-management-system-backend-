from flask import jsonify, request, Blueprint
from handlers.projects.project_list import ProjectList
from handlers.projects.project_details import ProjectDetails
from handlers.projects.project_contact_list import TeamUserProjList
from handlers.projects.project_create import ProjectCreate
from handlers.projects.project_edit import EditProject
from handlers.projects.project_edit_details import ProjectEditDetails
from middleware.token_middleware import token_required

proj_blueprint = Blueprint("proj_blueprint", __name__)

@proj_blueprint.route("/proj_list", methods=["POST"])
@token_required
def get_proj_list(current_app):
    response = ProjectList(request).get_proj_list()
    return jsonify(response)

@proj_blueprint.route("/proj_details", methods=["POST"])
@token_required
def get_proj_details(current_app):
    response = ProjectDetails(request).get_proj_details()
    return jsonify(response)

@proj_blueprint.route("/proj_contacts", methods=["POST"])
@token_required
def get_proj_contactlist(current_app):
    response = TeamUserProjList(request).get_list()
    return jsonify(response)


@proj_blueprint.route("/proj_create", methods=["POST"])
@token_required
def proj_create(current_app):
    response = ProjectCreate(request).addNewProj()
    return jsonify(response)

@proj_blueprint.route("/proj_edit", methods=["POST"])
@token_required
def proj_edit(current_app):
    response = EditProject(request).editNewProject()
    return jsonify(response)


@proj_blueprint.route("/get_proj_editform", methods=["POST"])
@token_required
def get_proj_editform(current_app):
    response = ProjectEditDetails(request).get_proj_details()
    return jsonify(response)