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
from schemas.user_schema import user_schema, UserSchema
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema
from models.watch_venue import WatchVenue
from schemas.watch_venue_schema import watch_venue_schema, watch_venues_schema
from models.watch_artist import WatchArtist
from schemas.watch_artist_schema import watch_artist_schema, watch_artists_schema


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(user_id)
    if not user:
        return abort(404, description="User does not exist")
    
    return jsonify(user_schema.dump(user))


@users.route("/<field>", methods=["PUT"])
@jwt_required()
def update_user(field):
    # GET THE id OF THE JWT ACCESS TOKEN FROM @jwt_required()
    user_id = int(get_jwt_identity())
    # RETRIEVE THE User OBJECT WITH THE id FROM get_jwt_identity() SO IT CAN BE UPDATED
    user = User.query.get(user_id)
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")
    
    # IF USER EXISTS, USE AS THE RECORD TO UPDATE    
    user_fields = user_schema.load(request.json, partial=True)
    # CHECK IF ARGUMENT FROM PATH PARAMETER MATCHES THE FOLLOWING ATTRIBUTES, AND IF SO THEN UPDATE THE CORRESPONDING COLUMN WITH THE VALUE FROM REQUEST FIELDS
    if field=="username":
        user.username = user_fields["username"]
    elif field=="password":
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    elif field=="email":
        user.email = user_fields["email"]
    elif field=="first_name":
        user.first_name = user_fields["first_name"]
    elif field=="last_name":
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
