from re import S
from main import db, bcrypt, jwt
from utils import search_table
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError
from sqlalchemy import func, desc, and_
from datetime import datetime, date, time, timedelta
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema, GigSchema
from models.performance import Performance
from schemas.performance_schema import performance_schema
from models.artist import Artist
from schemas.artist_schema import artist_schema, artists_schema
from models.user import User
from schemas.user_schema import user_schema, users_schema, UserSchema
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema
from models.watch_venue import WatchVenue
from schemas.watch_venue_schema import watch_venue_schema, watch_venues_schema
from models.watch_artist import WatchArtist
from schemas.watch_artist_schema import watch_artist_schema, watch_artists_schema


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/me", methods=["GET"])
@jwt_required()
def get_own_profile():
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(404, description="User does not exist")
    
    return jsonify(user_schema.dump(user))


@users.route("/", methods=["GET"])
@jwt_required()
def get_users():
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(404, description="User does not exist")
    # SEARCH USERS TABLE - BY DEFAULT RETURN ALL NON-ADMIN USERS BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    users = search_table(User, filters=[User.admin==False])
    
    return jsonify(users_schema.dump(users))


@users.route("/<int:user_id>", methods=["GET"])
def get_specific_user(user_id):
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(user_id)
    if not user:
        return abort(404, description="User does not exist")
    
    return jsonify(user_schema.dump(user))


@users.route("/form", methods=["GET"])
@jwt_required()
def get_user_form():
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(404, description="User does not exist")
    
    update_form = UserSchema(exclude=("id", "logged_in", "watched_venues", "watched_artists"))

    return jsonify(update_form.dump(user))
    

@users.route("/", methods=["PUT"])
@jwt_required()
def update_user():
    try: 
        user_fields = user_schema.load(request.json, partial=True)
    # IF INVALID, RETURN A DESCRIPTIVE ERROR
    except ValidationError as err:
        return jsonify(err.messages)
    # GET USER
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(401, description=Markup(f"User must be logged in"))
    # PARSE JSON DATA FROM REQUEST
    request_data = request.get_json()
    fields, new_values = [], []
    # PARSE COLUMNS TO UPDATE FROM THE REQUEST DATA
    for attribute in request_data.keys():
        # IF VALUE IS A VALID ATTRIBUTE OF USER
        if attribute in vars(User):
            if attribute == "password":
                setattr(user, attribute, bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8"))

            else:
                # SET THE ATTRIBUTE TO THE RELEVANT INPUT DATA
                setattr(user, attribute, user_fields[attribute])
                new_values.append(user_fields[attribute])
                fields.append(attribute)
    
    db.session.commit()

    updated_user = UserSchema(exclude=("watched_venues", "watched_artists"))

    return jsonify(message="Successfully updated profile", profile=updated_user.dump(user))




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


@users.route("/watchlist", methods=["GET"])
@jwt_required()
def get_watchlist():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")
    # CREATE WATCHLIST SCHEMA WHICH USES UserSchema BUT ONLY DISPLAYS username, watched_venues & watched_artists
    watchlist_schema = UserSchema(only=("username", "watched_venues", "watched_artists"))

    return jsonify(watchlist_schema.dump(user))
