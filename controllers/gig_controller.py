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
from models.user import User
from schemas.user_schema import user_schema


gigs = Blueprint("gigs", __name__, url_prefix="/gigs")


@gigs.route("/", methods=["GET"])
def show_all_gigs():
    # SELECT ALL RECORDS FROM THE gigs TABLE. IF NO RECORDS, RETURN DESCRIPTIVE MESSAGE
    gig_list = Gig.query.all()

    if not gig_list:
        return jsonify(message="Currently no gigs")

    return jsonify(gigs_schema.dump(gig_list))


@gigs.route("/", methods=["POST"])
@jwt_required()
def add_gig():
    gig_fields = gig_schema.load(request.json)
    gig = Gig(
        title = gig_fields["title"],
        description = gig_fields["description"],
        start_time = gig_fields["start_time"],
        price = gig_fields["price"],
        timestamp = datetime.now(),
        venue_id = gig_fields["venue_id"],
        user_id = get_jwt_identity(),    #### <----- GET user_id FROM CHECK ^^^
        artists = gig_fields["artists"]
    )
    db.session.add(gig)
    db.session.commit()

    artist_input = gig.artists.split(", ")
    for artist in artist_input:
        artist_exists = Artist.query.filter_by(name=artist).first()
        if not artist_exists:
            artist = Artist(
                name = artist
            )
            db.session.add(artist)
            db.session.commit()
        
            performance = Performance(
                gig_id = gig.id,
                artist_id = artist.id
            )
            db.session.add(performance)
            db.session.commit()
        
        else:
            performance = Performance(        # <------- REFACTOR / DRY
                gig_id = gig.id,
                artist_id = artist_exists.id
            )
            db.session.add(performance)
            db.session.commit()  

    return jsonify(gig_schema.dump(gig))


@gigs.route("/venues", methods=["GET"])
@jwt_required()
def gigs_watched_venues():
    # CHECK IF USER HAS VALID ACCESS TOKEN - IF YES RETURN USER'S id
    id = int(get_jwt_identity())
    # ATTEMPT RETRIEVE A User WITH THE id RETURNED FROM THE get_jwt_identity() FUNCTION
    user = User.query.get(id)
    if not user:
        return abort(404, description="Unauthorised - must be logged in")
    if user.id != id:
        return abort(401, description="Unauthorised")
