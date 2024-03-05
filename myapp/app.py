from flask import Flask
from flask_cors import CORS
from myapp.db import init_app
from myapp import settings
from models.load_models import load_db
from blueprints.auth_blueprint import auth_blueprint
from blueprints.user_blueprint import user_blueprint
from blueprints.dept_blueprint import dept_blueprint
from blueprints.proj_blueprint import proj_blueprint
from blueprints.team_blueprint import team_blueprint
from blueprints.chat_blueprint import char_blueprint
from blueprints.task_blueprint import task_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    settings.init(app)
    init_app(app)
    with app.app_context():
        load_db()
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(dept_blueprint, url_prefix="/dept")
    app.register_blueprint(proj_blueprint, url_prefix="/proj")
    app.register_blueprint(team_blueprint, url_prefix="/team")
    app.register_blueprint(char_blueprint, url_prefix="/chat")
    app.register_blueprint(task_blueprint, url_prefix="/tasks")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()