from flask import jsonify, request, Blueprint
from handlers.tasks.get_board import BoardDetails
from handlers.tasks.insert_task import TaskCreate
from handlers.tasks.insert_column import TaskTypeCreate
from handlers.tasks.reorder_list import ReorderStages
from handlers.tasks.update_task import EditTask
from middleware.token_middleware import token_required

task_blueprint = Blueprint("task_blueprint", __name__)

@task_blueprint.route("/board_details", methods=["POST"])
@token_required
def get_board_list(current_app):
    response = BoardDetails(request).get_board_details()
    return jsonify(response)

@task_blueprint.route("/task_contacts", methods=["POST"])
@token_required
def get_user_list(current_app):
    response = BoardDetails(request).get_project_users()
    return jsonify(response)

@task_blueprint.route("/create_tasks", methods=["POST"])
@token_required
def create_tasks(current_app):
    response = TaskCreate(request).addNewTask()
    return jsonify(response)

@task_blueprint.route("/update_task", methods=["POST"])
@token_required
def update_task(current_app):
    response = EditTask(request).editNewTask()
    return jsonify(response)

@task_blueprint.route("/delete_task", methods=["POST"])
@token_required
def delete_task(current_app):
    response = TaskCreate(request).delete_task()
    return jsonify(response)

@task_blueprint.route("/create_column", methods=["POST"])
@token_required
def create_column(current_app):
    response = TaskTypeCreate(request).addNewTaskType()
    return jsonify(response)

@task_blueprint.route("/delete_column", methods=["POST"])
@token_required
def delete_column(current_app):
    response = TaskTypeCreate(request).delete_column()
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

@task_blueprint.route("/update_col_tasks", methods=["POST"])
@token_required
def update_col_tasks(current_app):
    response = TaskTypeCreate(request).updateColumnTasks()
    return jsonify(response)