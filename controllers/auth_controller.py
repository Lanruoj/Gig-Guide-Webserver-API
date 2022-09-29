from flask import Blueprint, jsonify, request, abort, Markup
from main import db, bcrypt, jwt
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from models.user import User
from schemas.user_schema import user_schema


auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/", methods=["GET"])
def get_auth_template():
    user_template = {
        "email": "...",
        "username": "...",
        "password": "... [minimum 8 characters]",
        "first_name": "...",
        "last_name": "..."
    }
    return user_template


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
    
    user = User(
        username = user_fields["username"],
        email = user_fields["email"],
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"),
        first_name = user_fields["first_name"],
        last_name = user_fields["last_name"],
        logged_in = True
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))

    return jsonify(message=Markup(f"{user.first_name} successfully logged in"), user=user.username, id=user.id, token=token)


@auth.route("/login", methods=["POST"])
def auth_login():
    # username NOT REQUIRED FOR LOGIN
    user_fields = user_schema.load(request.json, partial=("username",))
    # SEARCH users FOR RECORD MATCHING THE INPUT email, ABORT IF NO EXISTING USER OR WRONG PASSWORD
    user = User.query.filter_by(email=user_fields["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Invalid email or password, please try again")
    
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    user.logged_in = True
    db.session.commit()
    
    return jsonify(token=token, user=user.username)


@auth.route("/logout", methods=["POST"])
@jwt_required()
def auth_logout():
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(400, description="User not logged in")
    
    user.logged_in = False
    db.session.commit()

    return jsonify(message=Markup(f"{user.username} successfully logged out"))
    
    


@auth.route("/<value>", methods=["PUT"])
@jwt_required()
def auth_update(value):
    # GET THE id OF THE JWT ACCESS TOKEN FROM @jwt_required()
    user_id = int(get_jwt_identity())
    # RETRIEVE THE User OBJECT WITH THE id FROM get_jwt_identity() SO IT CAN BE UPDATED
    user = User.query.get(user_id)
    
    # IF USER EXISTS, USE AS THE RECORD TO UPDATE    
    user_fields = user_schema.load(request.json, partial=True)

    if value=="username":
        user.username = user_fields["username"]
    elif value=="password":
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    elif value=="email":
        user.email = user_fields["email"]
    elif value=="first_name":
        user.first_name = user_fields["first_name"]
    elif value=="last_name":
        user.last_name = user_fields["last_name"]

    db.session.commit()

    return jsonify(user_schema.dump(user))


@auth.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def auth_delete(id):
    token_id = int(get_jwt_identity())
    user = User.query.get(token_id)
    if not user:
        return abort(401, description="Unauthorised - user must be logged in")
    if (user.id != id) and (not user.admin):
        return abort(401, description="Unauthorised - can only delete own profile")
    
    db.session.delete(user)
    db.session.commit()

    return jsonify(message=f"{user.username} has been deleted")
    
