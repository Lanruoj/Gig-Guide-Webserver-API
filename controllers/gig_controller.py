from main import db, bcrypt, jwt
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, date, time, timedelta
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema, GigSchema
from models.performance import Performance
from schemas.performance_schema import performance_schema
from models.artist import Artist
from schemas.artist_schema import artist_schema, artists_schema
from models.user import User
from schemas.user_schema import user_schema, UserSchema
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema
from models.watch_venue import WatchVenue
from schemas.watch_venue_schema import watch_venue_schema, watch_venues_schema
from models.watch_artist import WatchArtist
from schemas.watch_artist_schema import watch_artist_schema, watch_artists_schema


gigs = Blueprint("gigs", __name__, url_prefix="/gigs")


@gigs.route("/template", methods=["GET"])
def get_gig_template():
    gig_template = {
    "title": "...",
    "artists": "Artist 1, Artist 2, Artist 3",
    "venue_id": None,
    "description": "...",
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "price": None
    }
    return gig_template



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

    # CHECK IF GIG EXISTS WITHIN 2 HOURS OF GIG IN REQUEST
    gigs_at_this_venue = Gig.query.filter_by(venue_id=gig_fields["venue_id"]).all()
    new_gdt = datetime.strptime(gig_fields["start_time"], "%Y-%m-%d %H:%M:%S")
    for g in gigs_at_this_venue:
        delta = g.start_time - new_gdt
        if (g.start_time.date()==new_gdt.date()) and (delta < timedelta(days=0, hours=2)):
            return abort(409, description=f"{g.artists} has a gig within 2 hours of this at {g.venue.name}")

    gig = Gig(
        title = gig_fields["title"],
        description = gig_fields["description"],
        start_time = gig_fields["start_time"],
        price = gig_fields["price"],
        timestamp = datetime.now(),
        venue_id = gig_fields["venue_id"],
        user_id = get_jwt_identity(),
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


@gigs.route("/<int:gig_id>/<attr>", methods=["PUT"])
@jwt_required()
def update_gig(gig_id, attr):
    user = User.query.get(int(get_jwt_identity()))
    gig = Gig.query.filter(Gig.id==gig_id, Gig.user_id==user.id).first()
    if not gig:
        return abort(404, description=Markup(f"Invalid gig ID. Please try again"))
    if not user:
        return abort(401, description="Unauthorised - user must be logged in")
    if (user.id != gig.user_id):
        return abort(401, description="Unauthorised - user did not post the gig")

    gig_fields = gig_schema.load(request.json, partial=True)
    if attr == "title":
        gig.title = new_value = gig_fields["title"]
        new_value = gig_fields["title"]
        db.session.commit()
        return jsonify(message=Markup(f"{attr} updated to {new_value}"))

    if attr == "description":
        gig.description = gig_fields["description"]
        new_value = gig_fields["description"]
        db.session.commit()

    if attr == "start_time":
        gig.start_time = gig_fields["start_time"]
        new_value = gig_fields["start_time"]
        db.session.commit()

    if attr == "price":
        gig.price = gig_fields["price"]
        new_value = gig_fields["price"]
        db.session.commit()

    return jsonify(message=Markup(f"{attr} updated to {new_value} for the {gig.title} gig"))
        
    



@gigs.route("/watchlist", methods=["GET"])
@jwt_required()
def show_watchlist():
    # # GET THE id OF THE JWT ACCESS TOKEN FROM @jwt_required()
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    watchlist_schema = UserSchema(only=("username", "watched_venues", "watched_artists"))

    return jsonify(watchlist_schema.dump(user))