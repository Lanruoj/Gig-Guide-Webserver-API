from main import db, bcrypt, jwt
from utils import search_table, update_record
from flask import Blueprint, jsonify, request, abort, Markup
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


artists = Blueprint("artists", __name__, url_prefix="/artists")

@artists.route("/template", methods=["GET"])
def get_artist_template():
    artist_template = {
        "name": "...",
        "genre": "..."
    }

    return artist_template


@artists.route("/", methods=["GET"])
def search_artists():
    artists = search_table(Artist, artists_schema)

    return artists


@artists.route("/", methods=["POST"])
@jwt_required()
def add_artist():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.logged_in:
        return abort(401, description="User must be logged in")
    
    artist_fields = artist_schema.load(request.json)
    artist = Artist(
        name = artist_fields["name"],
        genre = artist_fields["genre"]
    )
    db.session.add(artist)
    db.session.commit()

    return jsonify(artist_schema.dump(artist))


@artists.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return jsonify(artist_schema.dump(artist))


@artists.route("/<int:artist_id>", methods=["PUT"])
@jwt_required()
def update_artist(artist_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.logged_in:
        return abort(401, description="User must be logged in")

    update = update_record(artist_id, Artist, artist_schema)

    db.session.commit()
    return update


@artists.route("/<int:artist_id>", methods=["DELETE"])
@jwt_required()
def delete_artist(artist_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user.admin or not user.logged_in:
        return abort(401, description="Unauthorised - must be an administrator to delete artists")
    
    artist = Artist.query.get(artist_id)
    if not artist:

        return abort(404, description="Artist does not exist")
    
    db.session.delete(artist)
    db.session.commit()

    return jsonify(message=f"{artist.name} has been deleted")



@artists.route("/watch", methods=["POST"])
@jwt_required()
def watch_artist():
    watch_artist_fields = watch_artist_schema.load(request.json)

    user = User.query.get(int(get_jwt_identity()))
    if not user or not user.logged_in:
        return abort(401, description="Unauthorised - user must be logged in")
        
    users_watched_artists = WatchArtist.query.filter_by(user_id=user.id).all()
    artist = Artist.query.get(watch_artist_fields["artist_id"])
    if not artist:

        return abort(404, description="Artist does not exist")

    for wa in users_watched_artists:
        if wa.artist_id ==  watch_artist_fields["artist_id"]:
            artist = Artist.query.get(watch_artist_fields["artist_id"])

            return abort(400, description=f"{user.first_name} already watching {artist.name}")
    

    new_watched_artist = WatchArtist(
        user_id = user.id,
        artist_id = watch_artist_fields["artist_id"]
    )
    db.session.add(new_watched_artist)
    db.session.commit()

    return jsonify(watch_artist_schema.dump(new_watched_artist))

