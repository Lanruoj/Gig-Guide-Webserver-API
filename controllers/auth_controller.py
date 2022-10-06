from flask import Blueprint, jsonify, request, abort, Markup
from main import db, bcrypt, jwt
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from models.user import User
from schemas.user_schema import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


# @auth.route("/register", methods=["GET"])
# def get_register_form():
#     # RETURN AN EMPTY USER JSON ARRAY TEMPLATE FOR THE USER TO USE TO REGISTER
#     user_template = {
#         "email": "...",
#         "username": "...",
#         "password": "... [minimum 8 characters]",
#         "first_name": "...",
#         "last_name": "..."
#     }
#     return user_template


@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)
    # CHECK IF THE username VALUE IN THE REQUEST EXISTS IN THE users TABLE. IF A MATCH IS FOUND, THROW A DESCRIPTIVE ERROR AS username MUST BE UNIQUE
    username_exists = User.query.filter_by(username=user_fields["username"]).first()
    if username_exists:
        return abort(409, f"Username {username_exists.username} already exists")
    # CHECK IF THE email VALUE IN THE REQUEST EXISTS IN THE users TABLE. IF A MATCH IS FOUND, THROW A DESCRIPTIVE ERROR AS email MUST BE UNIQUE
    email_exists = User.query.filter_by(email=user_fields["email"]).first()
    if email_exists:
        return abort(409, f"Email address {email_exists.email} already exists")
    # IF VALID REQUEST, CREATE NEW USER RECORD
    user = User(
        username = user_fields["username"],
        email = user_fields["email"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
        first_name = user_fields["first_name"],
        last_name = user_fields["last_name"],
        logged_in = True
    )
    # ADD NEW RECORD TO SESSION TO DATABASE AND COMMIT
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

    return jsonify(message=Markup(f"{user.first_name} successfully logged in"), user=user.username, id=user.id, token=token)


@auth.route("/login", methods=["GET"])
def get_login_form():
    # RETURN AN EMPTY USER JSON ARRAY TEMPLATE FOR THE USER TO LOGIN
    user_template = {
        "email": "...",
        "password": "..."
    }
    return user_template


@auth.route("/login", methods=["POST"])
def auth_login():
    # username NOT REQUIRED FOR LOGIN
    user_fields = user_schema.load(request.json, partial=True)
    # SEARCH users FOR RECORD MATCHING THE INPUT email, ABORT IF NO EXISTING USER OR WRONG PASSWORD
    user = User.query.filter_by(email=user_fields["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Invalid email or password, please try again")
    if user.logged_in:
        return abort(400, description="User already logged in")
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    # UPDATE USER'S logged_in ATTRIBUTE TO TRUE
    user.logged_in = True
    # COMMIT CHANGES TO DATABASE
    db.session.commit()

    return jsonify(token=token, user=user.username)


@auth.route("/logout", methods=["POST"])
@jwt_required()
def auth_logout():
    # FETCH USER FROM id RETURNED FROM JWT TOKEN USING get_jwt_identity() 
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(400, description="User not logged in")
    # UPDATE USER'S logged_in ATTRIBUTE TO FALSE
    user.logged_in = False
    # COMMIT CHANGES TO DATABASE
    db.session.commit()

    return jsonify(message=Markup(f"{user.username} successfully logged out"))