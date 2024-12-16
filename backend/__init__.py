import os
from flask import Flask, request
from flask_login import LoginManager
from flask_cors import CORS
from .database.create import User, engine
from sqlalchemy.orm import sessionmaker
from flask import jsonify
from flask_mail import Message
from .mail import mail

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Use test config if provided, otherwise use default config
    if test_config is None:
        app.config['SECRET_KEY'] = 'A'
        app.config['SESSION_COOKIE_SAMESITE'] = 'None'
        app.config['SESSION_COOKIE_SECURE'] = True
    else:
        app.config.update(test_config)
    # Email
    app.config["MAIL_SERVER"] = "in-v3.mailjet.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
    app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    
    mail.init_app(app)

    CORS(app, supports_credentials=True)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'
    login_manager.init_app(app)

    

    @login_manager.user_loader
    def load_user(user_id):
        return session.query(User).get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return {"success": "No", "reason": "Unauthorized"}, 401

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for profile routes in our app
    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    # blueprint for scholarships and internships routes in our app
    from .scholarships_internships import scholarships_internships
    app.register_blueprint(scholarships_internships)

    # blueprint for posts routes in our app
    from .posts import posts_bp as posts_blueprint
    app.register_blueprint(posts_blueprint)

    # blueprint for mentorship routes in our app
    from .mentorship import mentorship_bp as mentorship_blueprint
    app.register_blueprint(mentorship_blueprint)

    # Add a default route
    @app.route('/')
    def home():
        return jsonify(message="Welcome to the Financial Literacy Marketplace! Empowering you with the knowledge and tools to achieve financial success.")
    @app.route('/test_email', methods=["POST"])
    def emailing():
        msg = Message('Testing emailing for financial literacy!', sender='eltranscriber.email@gmail.com', recipients=[request.json["email"]])
        msg.body = f"Hey {request.json['name']}, \n Test was successful. Otherwise, you should not receive this email lol."
        mail.send(msg)
        return "sent"


    return app
