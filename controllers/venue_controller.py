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


venues = Blueprint("venues", __name__, url_prefix="/venues")

@venues.route("/", methods=["GET"])
def venues_show_all():
    venue_list = Venue.query.all()
    
    return jsonify(venues_schema.dump(venue_list))