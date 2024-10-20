from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request
from . import USERS, USER

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login_post():

    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = USERS.get(email.strip())

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user["password"], password):
        return {"success": "No"}  # if the user doesn't exist or password is wrong

    login_user(user, remember=remember)
    return {"success": "Yes"}


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = USERS.get(email.strip())  # if this returns a user, then the email already exists in database

    if user:  # if a user is already in the db, we do not add it again
        return {"success": "No"}

    # create a new user with the form data.
    USERS[email] = USER(
                    email=email,
                    name=name,
                    password=generate_password_hash(password),
                    id=email
                    )

    login_user(USERS[email], remember=True)
    return {"success": "Yes"}


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return {}


@auth.route('/ping')
def ping():
    return {"authenticated": current_user.is_authenticated}
