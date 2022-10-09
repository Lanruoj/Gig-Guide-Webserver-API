from main import db
from utils import search_table, update_record
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import exc
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema, VenueSchema
from models.user import User
from models.city import City
from schemas.city_schema import cities_schema
from models.venue_type import VenueType


venues = Blueprint("venues", __name__, url_prefix="/venues")


@venues.route("/search", methods=["GET"])
def get_venues():
    # SEARCH VENUES TABLE - BY DEFAULT RETURN ALL VENUES BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    venues = search_table(Venue)
    
    return jsonify(venues_schema.dump(venues)), 200


@venues.route("/<int:venue_id>", methods=["GET"])
def get_venue(venue_id):
    # FETCH VENUE FROM PATH PARAMETER'S venue_id
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(404, description=f"Venue does not exist")
    
    return jsonify(venue_schema.dump(venue)), 200


@venues.route("/new/form", methods=["GET"])
def get_new_venue_form():
    # RETURN AN EMPTY VENUE JSON ARRAY FOR USER TO ADD NEW VENUE WITH
    venue_template = {
    "name": "[string]",
    "genres": "[string: e.g Rock, Pop, Jazz -> http://localhost:5000/artists/genres",
    "country_id": "[integer: optional]"
    }
    return venue_template, 200


@venues.route("/new", methods=["POST"])
@jwt_required()
def venues_add():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    venue_fields = venue_schema.load(request.json, partial=True)
    # QUERY VENUE TABLE FOR A CASE INSENSITIVE MATCH FOR name IN REQUEST WITH MATCHING city (CHECK FOR DUPLICATE)
    input_venue_name = venue_fields["name"]
    input_city_id = venue_fields["city_id"]
    # QUERY CITY TABLE TO CHECK IF CITY EXISTS
    city_exists = City.query.filter(City.id==input_city_id).first()
    if not city_exists:
        return abort(422, description="Invalid city, search for cities at [GET] http://localhost:5000/venues/cities")

    venue_exists = Venue.query.filter(Venue.name.ilike(f"%{input_venue_name}%"), Venue.city_id==input_city_id).first()
    if venue_exists:
        return abort(409, description=Markup(f"A venue called {venue_exists.name} already exists in {venue_exists.city.name}. Location: [GET] http://localhost:5000/venues/{venue_exists.id}"))
    # IF VALID REQUEST, CREATE NEW VENUE RECORD
    venue = Venue(
        name = venue_fields["name"],
        street_address = venue_fields["street_address"],
        city_id = venue_fields["city_id"]
    )
    # OPTIONAL FIELDS
    request_data = request.get_json()
    if "venue_type_id" in request_data.keys():
        # QUERY VENUETYPE TABLE TO CHECK IF VENUE TYPE FROM REQUEST EXISTS
        type_exists = VenueType.query.filter(VenueType.id==venue_fields["venue_type_id"]).first()
        if not type_exists:
            return abort(422, description="Invalid venue type, get a list of valid types at [GET] http://localhost:5000/venues/types")
        else:
            venue.venue_type_id = venue_fields["venue_type_id"]

    # ADD NEW RECORD TO SESSION AND COMMIT TO DATABASE
    db.session.add(venue)
    db.session.commit()
    
    return jsonify(message="Venue successfully added", result=venue_schema.dump(venue), location=f"[GET] http://localhost:5000/venues/{venue.id}"), 201


@venues.route("/<int:venue_id>/form", methods=["GET"])
def get_venue_form(venue_id):
    # FETCH VENUE WITH id MATCHING venue_id FROM PATH PARAMETER
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(404, description="Venue does not exist")
    # CREATE FORM FOR USER TO UPDATE VENUE WITH
    update_form = VenueSchema(only=("name", "venue_type_id", "street_address", "city_id"))

    return jsonify(update_form.dump(venue)), 200


@venues.route("/<int:venue_id>", methods=["PUT"])
@jwt_required()
def update_venue(venue_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User must be logged in")
    # UPDATE VENUE FROM REQUEST BODY
    update = update_record(db, venue_id, Venue, venue_schema)
    if update[1]:
        return abort(422, description=Markup(f"Invalid value/s for {update[1]}. Please try again"))

    # IF VALID INPUT COMMIT CHANGES TO DATABASE
    db.session.commit()
    updated_schema = VenueSchema(exclude=("venue_gigs",))

    return jsonify(message="Venue successfully updated", venue=updated_schema.dump(update[0]), location=f"[GET] http://localhost:5000/venues/{update[0].id}"), 200


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


@venues.route("/cities", methods=["GET"])
def get_cities():
    # FETCH ALL CITIES BY DEFAULT OR TAKE QUERY STRING ARGUMENTS AS SEARCH/SORTING CRITERIA
    cities = search_table(City)

    return jsonify(cities_schema.dump(cities))


@venues.route("/types", methods=["GET"])
def get_venue_types():
    # FETCH ALL VENUE TYPES BY DEFAULT OR TAKE QUERY STRING ARGUMENTS AS SEARCH/SORTING CRITERIA
    types = search_table(VenueType)

    return jsonify(cities_schema.dump(types))