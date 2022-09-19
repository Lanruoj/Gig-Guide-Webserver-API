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


artists = Blueprint("artists", __name__, url_prefix="/artists")

@artists.route("/template", methods=["GET"])
def get_artist_template():
    artist_template = {
        "name": "...",
        "genre": "..."
    }

    return artist_template


@artists.route("/", methods=["GET"])
def show_all_artists():
    artist_list = Artist.query.all()
    return jsonify(artists_schema.dump(artist_list))