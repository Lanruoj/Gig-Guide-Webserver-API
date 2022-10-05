from flask import Blueprint, jsonify, request, abort, Markup
from main import db, bcrypt, jwt
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required
from models.user import User
from schemas.user_schema import user_schema


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/template", methods=["GET"])
def get_user_template():
    user_template = {
        "email": "...",
        "username": "...",
        "password": "... [minimum 8 characters]",
        "first_name": "...",
        "last_name": "..."
    }
    return user_template


@users.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return abort(404, description="User does not exist")
    
    return jsonify(user_schema.dump(user))


@users.route("/<value>", methods=["PUT"])
@jwt_required()
def update_user(value):
    # GET THE id OF THE JWT ACCESS TOKEN FROM @jwt_required()
    user_id = int(get_jwt_identity())
    # RETRIEVE THE User OBJECT WITH THE id FROM get_jwt_identity() SO IT CAN BE UPDATED
    user = User.query.get(user_id)
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")
    
    # IF USER EXISTS, USE AS THE RECORD TO UPDATE    
    user_fields = user_schema.load(request.json, partial=True)
    # CHECK IF ARGUMENT FROM PATH PARAMETER MATCHES THE FOLLOWING ATTRIBUTES, AND IF SO THEN UPDATE THE CORRESPONDING COLUMN WITH THE VALUE FROM REQUEST FIELDS
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
    # COMMIT CHANGES TO DATABASE
    db.session.commit()

    return jsonify(user_schema.dump(user))


@users.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    token_id = int(get_jwt_identity())
    # FETCH USER FROM USER TABLE USING PATH PAREMETER user_id
    user = User.query.get(user_id)
    if not user:
        return abort(401, description="Must be logged in to perform this action")
    if not user.admin:
        # IF token_id RETURNED FROM JWT TOKEN VIA get_jwt_identity() DOESN'T MATCH THE TARGET USER TO DELETE THEN ABORT
        if token_id != user_id:
            return abort(401, description="Must be an administrator to delete other profiles")
    # OTHERWISE, IF USER IS ADMIN OR OWNER OF PROFILE THEN DELETE USER AND COMMIT TO DATABASE
    db.session.delete(user)
    db.session.commit()

    return jsonify(message=f"{user.username} has been deleted")
