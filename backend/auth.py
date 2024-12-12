from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request
from sqlalchemy.orm import scoped_session, sessionmaker
from .database.create import User, engine

auth = Blueprint('auth', __name__)

# Create a scoped session
Session = sessionmaker(bind=engine)
session = scoped_session(Session)

@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        body = request.json
        email = body.get('email').strip()
        password = body.get('password')
        remember = True if body.get('remember') else False

        # Query the database for the user by email
        user = session.query(User).filter_by(email=email).first()

        # Check if user exists and verify password
        if not user or not check_password_hash(user.password_hash, password):
            return {"success": "No", "reason": "Invalid credentials"}

        # Login the user
        login_user(user, remember=remember)
        return {"success": "Yes"}

    elif request.method == "GET":
        return {"Authorization": "Unauthorized"}


@auth.route('/signup', methods=['POST'])
def signup_post():
    body = request.json
    email = body.get('email')
    if isinstance(email, str):
        email = email.strip()
    name = body.get('name')
    username = email  # body.get('username')
    password = body.get('password')

    # Validate input
    if not username:  # No field for username in the frontend
        return {"success": "No", "reason": "Username is required"}, 400
    if not email:
        return {"success": "No", "reason": "Email is required"}, 400
    if not password:
        return {"success": "No", "reason": "Password is required"}, 400

    # Check if user already exists in the database
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return {"success": "No", "reason": "User already exists with this username"}  # User already exists

    # Create a new user and add to the database
    try:
        new_user = User(
            email=email,
            name=name,
            password_hash=generate_password_hash(password),
            username=username
        )
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()  # Rollback on error
        return {"success": "No", "reason": f"Database error: {str(e)}"}, 500

    return {"success": "Yes"}


@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return {}, 200
    else:
        return {}, 401


@auth.route('/ping')
def ping():
    if current_user.is_authenticated:
        return {
            "authenticated": current_user.is_authenticated,
            "username": current_user.username,
            "id": current_user.user_id
        }
    return {"authenticated": current_user.is_authenticated}

