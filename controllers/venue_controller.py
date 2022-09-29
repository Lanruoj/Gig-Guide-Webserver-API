from main import db, bcrypt, jwt
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


@venues.route("/template", methods=["GET"])
def get_venue_template():
    venue_template = {
        "name": "...",
        "street_address": "...",
        "city": "...",
        "state": "...",
        "country": "...",
        "type": "... [e.g Music venue, Pub, Restaurant, Bar, Nightclub etc.]"
    }
    return venue_template


@venues.route("/", methods=["GET"])
def venues_show_all():
    venue_list = Venue.query.all()
    
    return jsonify(venues_schema.dump(venue_list))


@venues.route("/<venue_name>", methods=["GET"])
def search_for_venue(venue_name):
    venue = Venue.query.filter(Venue.name.match(venue_name)).all()
    if not venue:
        return abort(404, description="No venues exist with that name")
    
    result_schema = VenueSchema(exclude=("gigs",), many=True)
    return jsonify(result_schema.dump(venue))


@venues.route("/", methods=["POST"])
@jwt_required()
def venues_add():
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    venue_fields = venue_schema.load(request.json)
    venue_exists = Venue.query.filter(func.lower(Venue.name) == func.lower(venue_fields["name"]), func.lower(Venue.city) == func.lower(venue_fields["city"])).first()
    if venue_exists:
        return abort(409, description=Markup(f"A venue called {venue_exists.name} already exists in {venue_exists.city}. Venue ID: {venue_exists.id}"))
    
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
    db.session.add(venue)
    db.session.commit()
    
    return jsonify(venue_schema.dump(venue))


@venues.route("/<int:venue_id>/<attr>", methods=["PUT"])
@jwt_required()
def update_venue(venue_id, attr):
    user = User.query.get(get_jwt_identity())
    if not user.admin or not user.logged_in:
        return abort(401, description="Must be an administrator to perform this action")
    
    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(401, description=Markup(f"No venue with that ID exists"))
    
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
    user = User.query.get(int(get_jwt_identity()))
    if not user.admin or not user.logged_in:
        return abort(401, description="Must be an administrator to perform this action")

    venue = Venue.query.get(venue_id)
    if not venue:
        return abort(401, description=Markup(f"No venue with that ID exists"))
    
    if venue.gigs:
        return abort(409, description=Markup(f"Deletion cannot be performed because there are upcoming gigs at {venue.name}"))

    db.session.delete(venue)
    db.session.commit()

    return jsonify(message=Markup(f"{venue.name} has been deleted"))


@venues.route("/watch", methods=["POST"])
@jwt_required()
def add_watched_venue():
    watch_venue_fields = watch_venue_schema.load(request.json)

    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="Unauthorised - user must be logged in")
        
    users_watched_venues = WatchVenue.query.filter_by(user_id=user.id).all()
    venue_exists = Venue.query.get(watch_venue_fields["venue_id"])
    if not venue_exists:
        return abort(404, description="Venue does not exist")

    for wa in users_watched_venues:
        if wa.venue_id ==  watch_venue_fields["venue_id"]:
            venue = Venue.query.get(watch_venue_fields["venue_id"])
            return abort(400, description=f"{user.username} already watching {venue.name}")

    watch_venue = WatchVenue(
        user_id = user.id,
        venue_id = watch_venue_fields["venue_id"]
    )
    db.session.add(watch_venue)
    db.session.commit()

    return jsonify(watch_venue_schema.dump(watch_venue))