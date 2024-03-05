from flask import jsonify, request, Blueprint
from handlers.tasks.get_board import BoardDetails
from handlers.tasks.insert_task import TaskCreate
from handlers.tasks.insert_column import TaskTypeCreate
from handlers.tasks.reorder_list import ReorderStages
from middleware.token_middleware import token_required

task_blueprint = Blueprint("task_blueprint", __name__)

@task_blueprint.route("/board_details", methods=["POST"])
@token_required
def get_user_list(current_app):
    response = BoardDetails(request).get_board_details()
    return jsonify(response)

@task_blueprint.route("/create_tasks", methods=["POST"])
@token_required
def create_tasks(current_app):
    response = TaskCreate(request).addNewTask()
    return jsonify(response)

@task_blueprint.route("/create_column", methods=["POST"])
@token_required
def create_column(current_app):
    response = TaskTypeCreate(request).addNewTaskType()
    return jsonify(response)


@task_blueprint.route("/reorder_column", methods=["POST"])
@token_required
def reorder_column(current_app):
    response = ReorderStages(request).reorder()
    return jsonify(response)

@task_blueprint.route("/update_col_name", methods=["POST"])
@token_required
def update_col_name(current_app):
    response = ReorderStages(request).update_col_name()
    return jsonify(response)