# auth.py
# Uses current_app.session_factory() to get the session instead of global session.
# Ensures that tests can monkeypatch the session and that no NameError occurs.
from flask import Blueprint, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .database.create import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login_post():
    s = current_app.session_factory()  # Get session from current_app
    if request.method == 'POST':
        body = request.json
        email = body.get('email', '').strip()
        password = body.get('password')
        remember = True if body.get('remember') else False

        # Query user from DB
        user = s.query(User).filter_by(email=email).first()

        # Validate credentials
        if not user or not check_password_hash(user.password_hash, password):
            return {"success": "No", "reason": "Invalid credentials"}

        # Login sets session cookie managed by Flask-Login
        login_user(user, remember=remember)
        return {"success": "Yes"}

    # GET request returns Unauthorized info
    return {"Authorization": "Unauthorized"}

@auth.route('/signup', methods=['POST'])
def signup_post():
    s = current_app.session_factory()
    body = request.json
    email = body.get('email')
    if isinstance(email, str):
        email = email.strip()

    name = body.get('name')
    username = email
    password = body.get('password')
    bio = body.get('bio', '')  # Extract bio with a default value

    # Validate input fields
    if not username:
        return {"success": "No", "reason": "Username is required"}, 400
    if not email:
        return {"success": "No", "reason": "Email is required"}, 400
    if not password:
        return {"success": "No", "reason": "Password is required"}, 400

    # Check for existing user
    existing_user = s.query(User).filter_by(username=username).first()
    if existing_user:
        return {"success": "No", "reason": "User already exists with this username"}, 400

    # Create new user
    try:
        new_user = User(
            email=email,
            name=name,
            password_hash=generate_password_hash(password),
            username=username,
            bio=bio  # Add bio here
        )
        s.add(new_user)
        s.commit()
    except Exception as e:
        s.rollback()
        return {"success": "No", "reason": f"Database error: {str(e)}"}, 500

    return {"success": "Yes"}, 200


@auth.route('/logout')
def logout():
    # Logout if user is authenticated, else 401
    if current_user.is_authenticated:
        logout_user()
        return {}, 200
    else:
        return {}, 401

@auth.route('/ping')
def ping():
    # Check authentication status of current_user
    if current_user.is_authenticated:
        return {
            "authenticated": True,
            "username": current_user.username,  
            "id": current_user.user_id
        }
    return {"authenticated": False}
