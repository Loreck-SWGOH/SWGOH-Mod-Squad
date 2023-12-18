from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from .config import Config
from .db import DB


""" Specify where app goes when login is required """
login = LoginManager()
login.login_view = 'users.login'


def create_app():
    """ Add Bootstrap for CSS """
    app = Flask(__name__)
    app.config.from_object(Config)

    Bootstrap5(app)

    app.db = DB(app)
    login.init_app(app)

    from .controllers.index import bp as index_bp
    app.register_blueprint(index_bp)

    from .controllers.users import bp as user_bp
    app.register_blueprint(user_bp)

    from .controllers.admins import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
