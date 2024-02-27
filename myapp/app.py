from flask import Flask
from myapp.db import init_app
from myapp import settings
from blueprints.auth.auth_blueprint import auth_blueprint



def create_app():
    app = Flask(__name__)
    settings.init(app)
    init_app(app)
    app.register_blueprint(auth_blueprint, url_prefix="/api")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()