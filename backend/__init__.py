from flask import Flask
from flask_login import LoginManager, UserMixin
from flask_cors import CORS


# a variable to store users until we create a database for users
USERS = {}


class USER(UserMixin, dict):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'A'

    CORS(app, supports_credentials=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        # will be edited when we have a database
        return USERS[email]

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for profile routes in our app
    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app
