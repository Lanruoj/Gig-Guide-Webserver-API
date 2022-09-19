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
            return abort(400, description=f"{user.first_name} already watching <artist>")
    

    new_watched_artist = WatchArtist(
        user_id = user.id,
        artist_id = watch_artist_fields["artist_id"]
    )
    db.session.add(new_watched_artist)
    db.session.commit()

    return jsonify(watch_artist_schema.dump(new_watched_artist))

