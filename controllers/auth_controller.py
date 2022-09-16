from flask import Blueprint, jsonify, request, abort
from main import db, bcrypt, jwt
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.user import User
from schemas.user_schema import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)
    # CHECK IF A RECORD WITH THE INPUT username ALREADY EXISTS IN DATABASE - username MUST BE UNIQUE. IF IT DOES EXIST, THROW A DESCRIPTIVE ERROR MESSAGE. OTHERWISE, CREATE user OBJECT
    user = User.query.filter_by(username=user_fields["username"]).first()
    if user:
        return abort(409, "Username already exists")
    
    user = User(
        username = user_fields["username"],
        email = user_fields["email"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

    return jsonify(token)


@auth.route("/login", methods=["POST"])
def auth_login():
    # username NOT REQUIRED FOR LOGIN
    user_fields = user_schema.load(request.json, partial=("username",))
    user = User.query.filter_by(email=user_fields["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Invalid email or password, please try again")

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify(token=token, user=user.username)