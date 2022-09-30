from main import db, bcrypt, jwt
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import func, desc
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


@gigs.before_request
def gigs_before_request():
    expired_gigs = Gig.query.filter(Gig.start_time<datetime.now()).all()
    for gig in expired_gigs:
        gig.is_expired = True
        db.session.commit()


@gigs.route("/template", methods=["GET"])
def get_gig_template():
    gig_template = {
    "title": "...",
    "artists": "Artist 1, Artist 2, Artist 3",
    "venue_id": None,
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "description": "[string: optional]",
    "price": "[integer: optional]",
    "tickets_url": "[string: optional]"
    }
    return gig_template


@gigs.route("/", methods=["GET"])
def show_all_active_gigs():
    active_gigs = Gig.query.filter(Gig.is_deleted==False, Gig.is_expired==False).all()
    if not active_gigs:
        return jsonify(message="There are currently no upcoming gigs")
    

    ###
    if request.args.get("sort"):
        for attr_arg in request.args.values():
            attr = attr_arg.split(":", 1)[0]
            order = attr_arg.split(":", 1)[1]
            print(attr)
            print(order)
            if order == "asc":
                result = Gig.query.order_by(getattr(Gig, attr))
                return jsonify(gigs_schema.dump(result))
            elif order == "desc":
                result = Gig.query.order_by(desc(getattr(Gig, attr)))
                return jsonify(gigs_schema.dump(result))
    ###
        
    return jsonify(gigs_schema.dump(active_gigs))


@gigs.route("/<int:gig_id>", methods=["GET"])
def show_specific_gig(gig_id):
    gig = Gig.query.get(gig_id)
    if not gig:
        return abort(404, description=Markup(f"Gig not found with the ID of {gig_id}. Please try again"))
    
    return jsonify(gig_schema.dump(gig))


@gigs.route("/bin", methods=["GET"])
def show_inactive_gigs():
    # SELECT ALL RECORDS FROM THE gigs TABLE. IF NO RECORDS, RETURN DESCRIPTIVE MESSAGE
    inactive_gigs = Gig.query.filter((Gig.is_deleted==True) | (Gig.is_expired==True)).all()

    if not inactive_gigs:
        return jsonify(message="There are currently no inactive gigs")

    return jsonify(gigs_schema.dump(inactive_gigs))


@gigs.route("/", methods=["POST"])
@jwt_required()
def add_gig():
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")       
        
    gig_fields = gig_schema.load(request.json, partial=True)
    # CHECK IF GIG EXISTS WITHIN 2 HOURS OF GIG IN REQUEST
    active_gigs_at_this_venue = Gig.query.filter(Gig.venue_id==gig_fields["venue_id"], Gig.is_deleted==False).all()
    # new_gdt = datetime.strptime(gig_fields["start_time"], "%Y-%m-%d %H:%M:%S")
    for g in active_gigs_at_this_venue:
        delta = g.start_time - gig_fields["start_time"]
        if (g.start_time.date()==gig_fields["start_time"].date()) and (delta < timedelta(days=0, hours=2)):
            return abort(409, description=f"{g.artists} has a gig within 2 hours of this at {g.venue.name}")
    
    if gig_fields["start_time"] < datetime.now():
        return abort(409, description=Markup(f"Invalid input - start time must be in the future"))

    gig = Gig(
        title = gig_fields["title"],
        start_time = gig_fields["start_time"],
        timestamp = datetime.now(),
        venue_id = gig_fields["venue_id"],
        user_id = get_jwt_identity(),
        artists = gig_fields["artists"]
    )
    # OPTIONAL FIELDS
    request_data = request.get_json()
    if "tickets_url" in request_data.keys():
        gig.tickets_url = gig_fields["tickets_url"]
    if "price" in request_data.keys():
        gig.price = gig_fields["price"]
    if "description" in request_data.keys():
        gig.description = gig_fields["description"]
    db.session.add(gig)
    db.session.commit()


    artist_input = gig.artists.split(", ")
    for artist in artist_input:
        artist_exists = Artist.query.filter(func.lower(Artist.name)==(func.lower(artist))).first()
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
    if not user or not user.logged_in:
        return abort(401, description="Unauthorised - user must be logged in")
    if (user.id != gig.user_id):
        return abort(401, description="Unauthorised - user did not post the gig")

    gig_fields = gig_schema.load(request.json, partial=True)
    if attr == "title":
        gig.title = new_value = gig_fields["title"]
        new_value = gig_fields["title"]
        db.session.commit()
        return jsonify(message=Markup(f"Gig's {attr} updated to {new_value}"))

    elif attr == "description":
        gig.description = gig_fields["description"]
        new_value = gig_fields["description"]
        db.session.commit()

    elif attr == "start_time":
        gig.start_time = gig_fields["start_time"]
        new_value = gig_fields["start_time"]
        db.session.commit()

    elif attr == "price":
        gig.price = gig_fields["price"]
        new_value = gig_fields["price"]
        db.session.commit()

    return jsonify(message=Markup(f"{gig.title}'s {attr} updated to '{new_value}'"))
        

@gigs.route("/<int:gig_id>", methods=["DELETE"])
@jwt_required()
def delete_gig(gig_id):
    user = User.query.get(int(get_jwt_identity()))
    gig = Gig.query.get(gig_id)
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    if not gig:
        return abort(404, description=Markup(f"Gig doesn't exist with that ID"))

    user_created_gig = Gig.query.filter(Gig.user_id==user.id, Gig.id==gig_id).first()
    if not user_created_gig:
        return abort(401, description=Markup(f"User didn't create gig"))
    
    gig.is_deleted = True
    db.session.commit()

    return jsonify(message=Markup(f"{gig.title} has been deleted"))


@gigs.route("/watchlist", methods=["GET"])
@jwt_required()
def show_watchlist():
    # # GET THE id OF THE JWT ACCESS TOKEN FROM @jwt_required()
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    watchlist_schema = UserSchema(only=("username", "watched_venues", "watched_artists"))

    return jsonify(watchlist_schema.dump(user))