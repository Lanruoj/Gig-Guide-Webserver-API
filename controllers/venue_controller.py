from main import db, bcrypt, jwt
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema
from models.performance import Performance
from schemas.performance_schema import performance_schema
from models.artist import Artist
from schemas.artist_schema import artist_schema, artists_schema
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema
from models.user import User
from schemas.user_schema import user_schema


venues = Blueprint("venues", __name__, url_prefix="/venues")

@venues.route("/", methods=["GET"])
def venues_show_all():
    venue_list = Venue.query.all()
    
    return jsonify(venues_schema.dump(venue_list))


@venues.route("/", methods=["POST"])
@jwt_required()
def venues_add():
    user = User.query.get(int(get_jwt_identity()))
    if not user and not user.admin:
        return abort(401, description="Unauthorised")
    venue_fields = venue_schema.load(request.json)
    venue = Venue(
        name = venue_fields["name"],
        street_address = venue_fields["street_address"],
        city = venue_fields["city"],
        state = venue_fields["state"],
        country = venue_fields["country"]
    )
    db.session.add(venue)
    db.session.commit()
    
    return jsonify(venue_schema.dump(venue))
