# backend/__init__.py

from flask import Flask, jsonify
from flask_login import LoginManager
from flask_cors import CORS
from .database.create import User, engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

def create_app(test_config=None, session_factory=None):
    app = Flask(__name__)

    # Assign the session_factory
    if session_factory is None:
        Session = sessionmaker(bind=engine)
    else:
        Session = session_factory
    app.session_factory = Session

    # Use test config if provided, otherwise use default config
    if test_config is None:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
        app.config['SESSION_COOKIE_SAMESITE'] = 'None'
        app.config['SESSION_COOKIE_SECURE'] = True
    else:
        app.config.update(test_config)

    CORS(app, supports_credentials=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        User loader callback for Flask-Login.
        Directly uses app.session_factory to access the database session.
        """
        s = app.session_factory()
        return s.query(User).get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return {"success": "No", "reason": "Unauthorized"}, 401

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from .scholarships_internships import scholarships_internships
    app.register_blueprint(scholarships_internships)

    from .posts import posts_bp as posts_blueprint
    app.register_blueprint(posts_blueprint)

    from .mentorship import mentorship_bp as mentorship_blueprint
    app.register_blueprint(mentorship_blueprint)

    # Add a default route
    @app.route('/')
    def home():
        return jsonify(message="Welcome to the Financial Literacy Marketplace! Empowering you with the knowledge and tools to achieve financial success.")

    return app

# Removed 'app = create_app()' to prevent global app creation