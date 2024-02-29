from flask import jsonify, request, Blueprint
from handlers.departments.department_filter import DepartmentFilter
from handlers.departments.department_list import DepartmentList
from handlers.departments.department_details import DepartmentDetails
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