from flask import Flask
from flask_cors import CORS
from myapp.db import init_app
from myapp import settings
from models.load_models import load_db
from blueprints.auth.auth_blueprint import auth_blueprint
from blueprints.users.user_blueprint import user_blueprint
from blueprints.departments.dept_blueprint import dept_blueprint


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
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()