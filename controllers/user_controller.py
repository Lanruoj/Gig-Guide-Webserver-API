from re import S
from main import db, bcrypt
from utils import search_table
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError
from models.artist import Artist
from models.user import User
from schemas.user_schema import user_schema, UserSchema
from models.venue import Venue
from models.watch_venue import WatchVenue
from schemas.watch_venue_schema import watch_venue_schema
from models.watch_artist import WatchArtist
from schemas.watch_artist_schema import watch_artist_schema


users = Blueprint("users", __name__, url_prefix="/users")

profile_schema = UserSchema(only=("username", "first_name", "last_name", "watched_venues", "watched_artists"))
profiles_schema = UserSchema(only=("username", "first_name", "last_name", "watched_venues", "watched_artists"), many=True)


@users.route("/account", methods=["GET"])
@jwt_required()
def get_own_user_details():
    # FETCH USER WITH user_id PARSED FROM JWT IDENTITY FROM USER TABLE
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(404, description="User not logged in")
    
    return jsonify(user_schema.dump(user)), 200


@users.route("/profiles/search", methods=["GET"])
def search_profiles():
    # SEARCH USERS TABLE - BY DEFAULT RETURN ALL NON-ADMIN USERS BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    users = search_table(User, filters=[User.admin==False])
    
    return jsonify(profiles_schema.dump(users)), 200


@users.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_specific_users_details(user_id):
    # FETCH USER FROM JWT TOKEN IDENTITY
    user = User.query.get(get_jwt_identity())
    if not user.admin:
        return abort(401, description="Must be an administrator to perform this task")
    # FETCH TARGET USER WITH user_id FROM USER TABLE
    target_user = User.query.get(user_id)
    if not target_user:
        return abort(404, description="User not found")
    
    return jsonify(user_schema.dump(target_user)), 200


@users.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_user(user_id):
    # FETCH USER FROM JWT TOKEN IDENTITY
    user = User.query.get(get_jwt_identity())
    # IF USER IS NOT AN ADMINISTRATOR ABORT
    if not user.admin:
        return abort(401, description="Must be an administrator to delete other profiles")
    # FETCH USER TO DELETE FROM USER TABLE USING PATH PAREMETER user_id
    user_to_delete = User.query.get(user_id)
    # OTHERWISE, IF USER IS ADMIN OR OWNER OF PROFILE THEN DELETE USER AND COMMIT TO DATABASE
    db.session.delete(user_to_delete)
    db.session.commit()

    return jsonify(message=f"{user_to_delete.username} has been deleted"), 200


@users.route("/profiles", methods=["GET"])
@jwt_required()
def get_own_profile():
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(404, description="User not logged in")
    
    return jsonify(profile_schema.dump(user)), 200


@users.route("/profiles/<int:user_id>", methods=["GET"])
def get_specific_users_profile(user_id):
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(user_id)
    if not user:
        return abort(404, description="User does not exist")
    
    return jsonify(profile_schema.dump(user)), 200


@users.route("/profiles/form", methods=["GET"])
@jwt_required()
def get_user_update_form():
    # FETCH USER WITH user_id FROM USER TABLE
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(404, description="User does not exist")
    
    update_form = UserSchema(exclude=("id", "logged_in", "watched_venues", "watched_artists"))

    return jsonify(update_form.dump(user)), 200
    

@users.route("/profiles", methods=["PUT"])
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

    updated_user_schema = UserSchema(exclude=("watched_venues", "watched_artists"))

    return jsonify(message="Profile successfully updated", profile=updated_user_schema.dump(user), location=f"[GET] http://localhost:5000/users/profile/{user.id}"), 200


@users.route("/profiles", methods=["DELETE"])
@jwt_required()
def delete_own_profile():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user:
        return abort(401, description="Must be logged in to perform this action")
    # OTHERWISE, IF JWT TOKEN IS VALID AND USER IS FOUND THEN DELETE USER FROM DATABASE AND COMMIT
    db.session.delete(user)
    db.session.commit()

    return jsonify(message=f"{user.username} has been deleted"), 200


@users.route("/watchlist", methods=["GET"])
@jwt_required()
def get_watchlist():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")
    # CREATE WATCHLIST SCHEMA WHICH USES UserSchema BUT ONLY DISPLAYS username, watched_venues & watched_artists
    watchlist_schema = UserSchema(only=("username", "watched_venues", "watched_artists"))

    return jsonify(watchlist_schema.dump(user)), 200


@users.route("/watchlist/form", methods=["GET"])
def watch_form():
    watch_template = {
        "artist_id / venue_id": "[integer]"
    }

    return watch_template, 200


@users.route("/watchlist", methods=["POST"])
@jwt_required()
def add_to_watchlist():
    # SEARCH THROUGH REQUEST BODY FOR ID FOR ARTIST/VENUE TO WATCH
    request_data = request.get_json()
    if "venue_id" in request_data.keys():
        watch_venue_fields = watch_venue_schema.load(request.json, partial=True)
        # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
        user = User.query.get(int(get_jwt_identity()))
        if not user or not user.logged_in:
            return abort(401, description="Unauthorised - user must be logged in")
        # FETCH USERS WATCHVENUE RECORDS FILTERED BY user_id FROM FETCHED USER
        users_watched_venues = WatchVenue.query.filter_by(user_id=user.id).all()
        # CHECK IF VENUE WITH REQUEST'S venue_id EXISTS IN VENUE TABLE
        venue_exists = Venue.query.get(watch_venue_fields["venue_id"])
        if not venue_exists:
            return abort(404, description="Venue does not exist")
        # LOOK THROUGH ALL OF USER'S WATCHED VENUES TO CHECK IF USER IS ALREADY WATCHING THE VENUE FROM THE REQUEST (CHECK FOR DUPLICATE)
        for wa in users_watched_venues:
            if wa.venue_id ==  watch_venue_fields["venue_id"]:
                # IF venue_id ALREADY IN USER'S WATCHED VENUE, FETCH VENUE'S NAME FOR DESCRIPTIVE MESSAGE
                venue = Venue.query.get(watch_venue_fields["venue_id"])
                return abort(400, description=f"{user.username} already watching {venue.name}")
        # IF VALID REQUEST, CREATE NEW WATCHVENUE RECORD
        watch_venue = WatchVenue(
            user_id = user.id,
            venue_id = watch_venue_fields["venue_id"]
        )
        # ADD NEW RECORD TO DATABASE AND COMMIT
        db.session.add(watch_venue)
        db.session.commit()

        return jsonify(message=f"You are now watching {venue_exists.name}", result=watch_venue_schema.dump(watch_venue)), 201
    
    elif "artist_id" in request_data.keys():
        watch_artist_fields = watch_artist_schema.load(request.json, partial=True)
        # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
        user = User.query.get(int(get_jwt_identity()))
        if not user or not user.logged_in:
            return abort(401, description="User must be logged in")
        # FETCH USER'S WATCHED ARTISTS FROM THE WATCHARTISTS TABLE
        users_watched_artists = WatchArtist.query.filter_by(user_id=user.id).all()
        # FETCH ARTIST FROM THE REQUEST BODY'S artist_id
        artist = Artist.query.get(watch_artist_fields["artist_id"])
        if not artist:
            return abort(404, description="Artist does not exist")
        # LOOK THROUGH ALL OF USER'S WATCHED ARTISTS TO CHECK IF USER IS ALREADY WATCHING THE ARTIST FROM THE REQUEST (CHECK FOR DUPLICATE)
        for wa in users_watched_artists:
            if wa.artist_id == watch_artist_fields["artist_id"]:
                # IF artist_id ALREADY IN USER'S WATCHED ARTISTS, FETCH ARTIST'S NAME FOR DESCRIPTIVE MESSAGE
                artist = Artist.query.get(watch_artist_fields["artist_id"])

                return abort(409, description=f"{user.first_name} already watching {artist.name}")
        
        # IF VALID REQUEST CREATE NEW WATCHARTIST RECORD
        new_watched_artist = WatchArtist(
            user_id = user.id,
            artist_id = watch_artist_fields["artist_id"]
        )
        # ADD NEW RECORD TO SESSION AND COMMIT TO DATABASE
        db.session.add(new_watched_artist)
        db.session.commit()

        return jsonify(message=f"You are now watching {artist.name}", result=watch_artist_schema.dump(new_watched_artist)), 201
    
    else:
        return abort(404, description="Invalid field name/s")


@users.route("/watchlist", methods=["DELETE"])
@jwt_required()
def delete_watched_item():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return abort(401, description="User must be logged in")
    # SEARCH THROUGH REQUEST BODY FOR ID OF ARTIST/VENUE TO BE DELETED
    request_data = request.get_json()
    if "venue_id" in request_data.keys():
        # FETCH VENUE FROM PATH PARAMETER WITH MATCHING id
        venue = Venue.query.get(request_data["venue_id"])
        if not venue:
            return abort(404, description="Venue not found")
        # CHECK IF THERE EXISTS A WATCHVENUE RECORD WITH THE CURRENT USER'S ID AND THE VENUE'S ID
        watched_venue = WatchVenue.query.filter(WatchVenue.venue_id==request_data["venue_id"], WatchVenue.user_id==user.id).first()
        if not watched_venue:
            return abort(404, description=f"User is not following {venue.name}")
        # DELETE WATCHARTIST RECORD FROM SESSION AND COMMIT TO DATABASE
        db.session.delete(watched_venue)
        db.session.commit()

        return jsonify(message=f"{venue.name} has been successfully removed from your watchlist"), 200
        
    elif "artist_id" in request_data.keys():
        # FETCH ARTIST FROM PATH PARAMETER WITH MATCHING id
        artist = Artist.query.get(request_data["artist_id"])
        if not artist:
            return abort(404, description="Artist not found")
        # CHECK IF THERE EXISTS A WATCHARTIST RECORD WITH THE CURRENT USER'S ID AND THE ARTIST'S ID
        watched_artist = WatchArtist.query.filter(WatchArtist.artist_id==request_data["artist_id"], WatchArtist.user_id==user.id).first()
        if not watched_artist:
            return abort(404, description=f"User is not following {artist.name}")
        # DELETE WATCHARTIST RECORD FROM SESSION AND COMMIT TO DATABASE
        db.session.delete(watched_artist)
        db.session.commit()

        return jsonify(message=f"{artist.name} has been successfully removed from your watchlist"), 200
    
    else:
        return abort(404, description="Invalid field name/s")