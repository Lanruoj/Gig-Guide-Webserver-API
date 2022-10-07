from main import db, bcrypt, jwt
from utils import search_table, update_record
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


@venues.route("/", methods=["GET"])
def get_venues():
    # SEARCH VENUES TABLE - BY DEFAULT RETURN ALL VENUES BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    venues = search_table(Venue)
    
    return jsonify(venues_schema.dump(venues)), 200


@venues.route("/<int:venue_id>", methods=["GET"])
def get_venue(venue_id):
    # FETCH VENUE FROM PATH PARAMETER'S venue_id
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(404, description=f"No venues exist with ID={venue_id}")
    
    return jsonify(venue_schema.dump(venue)), 200


@venues.route("/new/form", methods=["GET"])
def get_new_venue_form():
    # RETURN AN EMPTY VENUE JSON ARRAY FOR USER TO ADD NEW VENUE WITH
    venue_template = {
        "name": "...",
        "street_address": "...",
        "city": "...",
        "state": "...",
        "country": "...",
        "type": "... [e.g Music venue, Pub, Restaurant, Bar, Nightclub etc.]"
    }
    return venue_template, 200


@venues.route("/new", methods=["POST"])
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
    
    return jsonify(result=venue_schema.dump(venue), location=f"http://localhost:5000/venues/{venue.id}"), 201


@venues.route("/<int:venue_id>/form", methods=["GET"])
def get_venue_form(venue_id):
    # FETCH VENUE WITH id MATCHING venue_id FROM PATH PARAMETER
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(404, description="Venue does not exist")
    # CREATE FORM FOR USER TO UPDATE VENUE WITH
    update_form = VenueSchema(exclude=("id", "venue_gigs"))

    return jsonify(update_form.dump(venue)), 200


@venues.route("/<int:venue_id>", methods=["PUT"])
@jwt_required()
def update_venue(venue_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User must be logged in")
    # UPDATE VENUE FROM REQUEST BODY
    update = update_record(venue_id, Venue, venue_schema)
    # COMMIT CHANGES TO DATABASE
    db.session.commit()

    updated_schema = VenueSchema(exclude=("venue_gigs",))

    return jsonify(message="Venue successfully updated", venue=updated_schema.dump(update)), 200


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

    return jsonify(message=Markup(f"{venue.name} has been deleted")), 200