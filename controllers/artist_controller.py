from main import db, bcrypt, jwt
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema
from models.performance import Performance
from schemas.performance_schema import performance_schema
from models.artist import Artist
from schemas.artist_schema import artist_schema, artists_schema
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
def show_all_artists():
    artist_list = Artist.query.all()

    return jsonify(artists_schema.dump(artist_list))


@artists.route("/", methods=["POST"])
@jwt_required()
def add_artist():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return abort(401, description="Unauthorised, must be logged in")
    
    artist_fields = artist_schema.load(request.json)
    artist = Artist(
        name = artist_fields["name"],
        genre = artist_fields["genre"]
    )
    db.session.add(artist)
    db.session.commit()

    return jsonify(artist_schema.dump(artist))


@artists.route("/<int:artist_id>/<attr>", methods=["PUT"])
@jwt_required()
def update_artist(artist_id, attr):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return abort(401, description="Unauthorised - must be logged in to update artists")

    artist_fields = artist_schema.load(request.json, partial=True)
    
    artist = Artist.query.get(artist_id)
    if not artist:
        return abort(404, description="Artist does not exist")

    if attr == "name":
        old_name = artist.name
        artist.name = artist_fields["name"]
        db.session.commit()

        return jsonify(message=Markup(f"{old_name}'s name updated to '{artist.name}'"))

    if attr == "genre":
        new_genre = artist_fields["genre"]
        artist.genre = new_genre
        db.session.commit()

        return jsonify(message=Markup(f"{artist.name}'s genre updated to '{new_genre}'"))

    else:

        return abort(400, description=Markup(f"'{attr}' is not a valid argument. Attributes that can be updated are 'name' and 'genre"))



@artists.route("/<int:artist_id>", methods=["DELETE"])
@jwt_required()
def delete_artist(artist_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user.admin:
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

