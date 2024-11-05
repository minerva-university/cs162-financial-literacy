from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from .database.create import User, engine
from sqlalchemy.orm import sessionmaker


# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'A'

    CORS(app, supports_credentials=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'
    login_manager.init_app(app)

    

    @login_manager.user_loader
    def load_user(user_id):
        return session.query(User).get(int(user_id))

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

    return app
