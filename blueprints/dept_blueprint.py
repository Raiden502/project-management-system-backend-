from flask import jsonify, request, Blueprint
from handlers.departments.department_filter import DepartmentFilter
from handlers.departments.department_list import DepartmentList
from handlers.departments.department_details import DepartmentDetails
from handlers.departments.department_create import CreateDept
from handlers.departments.department_edit import EditDept
from handlers.departments.get_team_user import TeamUserDeptList
from handlers.departments.department_details_edit import DepartmentEditDetails
from handlers.departments.department_delete import DeleteDepartment
from middleware.token_middleware import token_required

dept_blueprint = Blueprint("dept_blueprint", __name__)

@dept_blueprint.route("/dept_filter", methods=["POST"])
@token_required
def get_dept_filter(current_app):
    response = DepartmentFilter(request).get_filter_list()
    return jsonify(response)

@dept_blueprint.route("/dept_list", methods=["POST"])
@token_required
def get_dept_list(current_app):
    response = DepartmentList(request).get_dept_list()
    return jsonify(response)

@dept_blueprint.route("/dept_details", methods=["POST"])
@token_required
def get_dept_details(current_app):
    response = DepartmentDetails(request).get_dept_details()
    return jsonify(response)

@dept_blueprint.route("/create_dept", methods=["POST"])
@token_required
def create_dept(current_app):
    response = CreateDept(request).addNewDept()
    return jsonify(response)

@dept_blueprint.route("/edit_dept", methods=["POST"])
@token_required
def edit_dept(current_app):
    response = EditDept(request).editNewDept()
    return jsonify(response)

@dept_blueprint.route("/get_dept_contacts", methods=["POST"])
@token_required
def get_user_team_list(current_app):
    response = TeamUserDeptList(request).get_list()
    return jsonify(response)

@dept_blueprint.route("/get_dept_editdetails", methods=["POST"])
@token_required
def get_dept_editdetails(current_app):
    response = DepartmentEditDetails(request).get_dept_details()
    return jsonify(response)

@dept_blueprint.route("/dept_delete", methods=["POST"])
@token_required
def dept_delete(current_app):
    response = DeleteDepartment(request).delete()
    return jsonify(response)