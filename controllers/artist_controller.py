from main import db, bcrypt, jwt
from utils import search_table, update_record
from flask import Blueprint, jsonify, request, abort, Markup, Response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError
from datetime import datetime
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema
from models.performance import Performance
from schemas.performance_schema import performance_schema
from models.artist import Artist
from schemas.artist_schema import artist_schema, artists_schema, ArtistSchema
from models.watch_artist import WatchArtist
from schemas.watch_artist_schema import watch_artist_schema
from models.user import User
from schemas.user_schema import user_schema
from models.genre import Genre
from schemas.genre_schema import genres_schema


artists = Blueprint("artists", __name__, url_prefix="/artists")


@artists.route("/", methods=["GET"])
def get_artists():
    # SEARCH ARTISTS TABLE - BY DEFAULT RETURN ALL BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    artists = search_table(Artist)
    
    return jsonify(artists_schema.dump(artists)), 200


@artists.route("/new/form", methods=["GET"])
def get_new_artist_form():
    # RETURN AN EMPTY ARTIST JSON ARRAY TEMPLATE
    artist_template = {
        "name": "[string]"
    }

    return artist_template, 200
    

@artists.route("/new", methods=["POST"])
@jwt_required()
def add_artist():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User must be logged in")
    
    artist_fields = artist_schema.load(request.json)
    # QUERY DATABASE TO CHECK IF ARTIST ALREADY EXISTS WITH THE REQUEST'S name
    artist_exists = Artist.query.filter(Artist.name.ilike(f"%{artist_fields['name']}%")).first()
    if artist_exists:
        return abort(409, description=f"An artist already exists called {artist_fields['name']}")

    # CREATE NEW ARTIST FROM REQUEST FIELDS
    artist = Artist(
        name = artist_fields["name"]
    )
    # ADD ARTIST TO SESSION AND COMMIT TO DATABASE
    db.session.add(artist)
    db.session.commit()

    return jsonify(result=artist_schema.dump(artist), location=f"http://localhost:5000/artists/{artist.id}"), 201


@artists.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    # FETCH ARTIST WITH id MATCHING artist_id FROM PATH PARAMETER
    artist = Artist.query.get(artist_id)
    if not artist:
        return abort(404, description="Artist does not exist")

    return jsonify(artist_schema.dump(artist)), 200


@artists.route("/<int:artist_id>/form", methods=["GET"])
def get_artist_form(artist_id):
    # FETCH ARTIST WITH id MATCHING artist_id FROM PATH PARAMETER
    artist = Artist.query.get(artist_id)
    if not artist:
        return abort(404, description="Artist does not exist")
    # CREATE FORM FOR USER TO UPDATE ARTIST WITH
    update_form = ArtistSchema(exclude=("id", "performances"))

    return jsonify(update_form.dump(artist)), 200


@artists.route("/<int:artist_id>", methods=["PUT"])
@jwt_required()
def update_artist(artist_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="User must be logged in")
    # UPDATE ARTIST FROM REQUEST BODY
    artist = update_record(artist_id, Artist, artist_schema)
    # COMMIT CHANGES TO DATABASE
    db.session.commit()

    return jsonify(result=artist_schema.dump(artist), location=f"http://localhost:5000/artists/{artist.id}"), 200


@artists.route("/<int:artist_id>", methods=["DELETE"])
@jwt_required()
def delete_artist(artist_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    if not user.admin or not user.logged_in:
        return abort(401, description="Unauthorised - must be an administrator to delete artists")
    # FETCH ARTIST FROM PATH PARAMETER WITH MATCHING id
    artist = Artist.query.get(artist_id)
    if not artist:
        return abort(404, description="Artist does not exist")
    # DELETE ARTIST FROM SESSION AND COMMIT TO DATABASE
    db.session.delete(artist)
    db.session.commit()

    return jsonify(message=f"{artist.name} has been successfully deleted"), 200


@artists.route("/genres", methods=["GET"])
def get_genres():
    # SEARCH GENRES TABLE - BY DEFAULT RETURN ALL GENRES BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    genres = search_table(Genre)

    return jsonify(genres_schema.dump(genres))

