from main import db, bcrypt, jwt
from utils import search_table
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import func
from datetime import datetime
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema
from models.performance import Performance
from schemas.performance_schema import performance_schema
from models.artist import Artist
from schemas.artist_schema import artist_schema, artists_schema
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema, VenueSchema
from models.user import User
from schemas.user_schema import user_schema
from models.watch_venue import WatchVenue
from schemas.watch_venue_schema import watch_venue_schema


venues = Blueprint("venues", __name__, url_prefix="/venues")


# @venues.route("/template", methods=["GET"])
# def get_venue_template():
#     venue_template = {
#         "name": "...",
#         "street_address": "...",
#         "city": "...",
#         "state": "...",
#         "country": "...",
#         "type": "... [e.g Music venue, Pub, Restaurant, Bar, Nightclub etc.]"
#     }
#     return venue_template


@venues.route("/", methods=["GET"])
def get_venues():
    # SEARCH VENUES TABLE - BY DEFAULT RETURN ALL VENUES BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    venues = search_table(Venue)
    
    return jsonify(venues_schema.dump(venues))


@venues.route("/<int:venue_id>", methods=["GET"])
def get_venue(venue_id):
    # FETCH VENUE FROM PATH PARAMETER'S venue_id
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(404, description=f"No venues exist with ID={venue_id}")
    
    return jsonify(venue_schema.dump(venue))


@venues.route("/new", methods=["GET"])
def get_new_venue_form():
    venue_template = {
        "name": "...",
        "street_address": "...",
        "city": "...",
        "state": "...",
        "country": "...",
        "type": "... [e.g Music venue, Pub, Restaurant, Bar, Nightclub etc.]"
    }
    return venue_template


@venues.route("/", methods=["POST"])
@jwt_required()
def venues_add():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    venue_fields = venue_schema.load(request.json)
    # QUERY VENUE TABLE FOR A CASE INSENSITIVE MATCH FOR name IN REQUEST WITH MATCHING city (CHECK FOR DUPLICATE)
    venue_exists = Venue.query.filter(func.lower(Venue.name) == func.lower(venue_fields["name"]), func.lower(Venue.city) == func.lower(venue_fields["city"])).first()
    if venue_exists:
        return abort(409, description=Markup(f"A venue called {venue_exists.name} already exists in {venue_exists.city}. Venue ID: {venue_exists.id}"))
    # IF VALID REQUEST, CREATE NEW VENUE RECORD
    venue = Venue(
        name = venue_fields["name"],
        street_address = venue_fields["street_address"],
        city = venue_fields["city"],
        state = venue_fields["state"],
        country = venue_fields["country"]
    )
    # OPTIONAL FIELDS
    request_data = request.get_json()
    if "type" in request_data.keys():
        venue.type = venue_fields["type"]
    # ADD NEW RECORD TO SESSION AND COMMIT TO DATABASE
    db.session.add(venue)
    db.session.commit()
    
    return jsonify(venue_schema.dump(venue))


@venues.route("/<int:venue_id>/<attr>", methods=["PUT"])
@jwt_required()
def update_venue(venue_id, attr):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user.admin or not user.logged_in:
        return abort(401, description="Must be an administrator to perform this action")
    # FETCH VENUE FROM VENUES TABLE WITH MATCHING venue_id FROM PATH PARAMETERS
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(401, description=Markup(f"No venue with that ID exists"))
    # CHECK IF ARGUMENT FROM PATH PARAMETER MATCHES THE FOLLOWING ATTRIBUTES, AND IF SO THEN UPDATE THE CORRESPONDING COLUMN WITH THE VALUE FROM REQUEST FIELDS
    venue_fields = venue_schema.load(request.json, partial=True)
    if attr == "name":
        venue.name = venue_fields["name"]
    if attr == "street_address":
        venue.street_address = venue_fields["street_address"]
    if attr == "city":
        venue.city = venue_fields["city"]
    if attr == "state":
        venue.state = venue_fields["state"]
    if attr == "country":
        venue.country = venue_fields["country"]
    if attr == "type":
        venue.type = venue_fields["type"]
    
    return jsonify(venue_schema.dump(venue))


@venues.route("/<int:venue_id>", methods=["DELETE"])
@jwt_required()
def delete_venue(venue_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user.admin:
        return abort(401, description="Must be an administrator to perform this action")
    # FETCH VENUE FROM VENUES TABLE WITH MATCHING venue_id FROM PATH PARAMETERS
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(401, description=Markup(f"No venues found with ID={venue_id}"))
    # ADD NEW RECORD TO SESSION AND COMMIT TO DATABASE
    db.session.delete(venue)
    db.session.commit()

    return jsonify(message=Markup(f"{venue.name} has been deleted"))


@venues.route("/watch", methods=["POST"])
@jwt_required()
def add_watched_venue():
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

    return jsonify(watch_venue_schema.dump(watch_venue))