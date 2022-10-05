from re import S
from main import db, bcrypt, jwt
from utils import search_table
from flask import Blueprint, jsonify, request, abort, Markup
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from marshmallow.exceptions import ValidationError
from sqlalchemy import func, desc, and_
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
    # BEFORE EACH REQUEST IS EXECUTED, SET ALL GIGS WITH start_time IN THE PAST AS EXPIRED (is_expired=True)
    expired_gigs = Gig.query.filter(Gig.start_time<datetime.now()).all()
    for gig in expired_gigs:
        gig.is_expired = True
        db.session.commit()


@gigs.route("/template", methods=["GET"])
def get_gig_template():
    # RETURN AN EMPTY GIG JSON ARRAY TEMPLATE FOR THE USER TO USE
    gig_template = {
    "title": "...",
    "artists": "Artist 1, Artist 2, Artist 3",
    "venue_id": None,
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "description": "[string: optional]",
    "price": "[integer: optional]",
    "tickets_url": "https://...[string: optional]"
    }
    return gig_template


@gigs.route("/", methods=["GET"])
def get_gigs():
    # SEARCH GIGS TABLE - BY DEFAULT RETURN ALL NON-EXPIRED GIGS BUT TAKES OPTIONAL QUERY STRING ARGUMENTS FOR FILTERING AND SORTING
    gigs = search_table(Gig, filters=[Gig.is_expired==False], sort=Gig.date_added)

    return jsonify(gigs_schema.dump(gigs))


@gigs.route("/<int:gig_id>", methods=["GET"])
def show_specific_gig(gig_id):
    # QUERY GIGS FOR GIG WITH ID OF gig_id
    gig = Gig.query.get(gig_id)
    if not gig:
        return abort(404, description=Markup(f"Gig not found with the ID of {gig_id}. Please try again"))

    return jsonify(gig_schema.dump(gig))


@gigs.route("/bin", methods=["GET"])
def show_expired_gigs():
    # SELECT ALL RECORDS FROM THE GIGS TABLE WITH is_expired=True
    expired_gigs = search_table(Gig, filters=[Gig.is_expired==True])
    if not expired_gigs:
        return jsonify(message="There are currently no expired gigs")

    return jsonify(gigs_schema.dump(expired_gigs))


@gigs.route("/", methods=["POST"])
@jwt_required()
def add_gig():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")    

    gig_fields = gig_schema.load(request.json, partial=True)
    # CHECK IF VENUE WITH venue_id IN REQUEST EXISTS IN VENUE TABLE 
    venue = Venue.query.get(gig_fields["venue_id"])
    if not venue:
        return abort(400, description=f"Invalid venue (ID={gig_fields['venue_id']})")
    # GET A LIST OF ALL ACTIVE GIGS WITH THE SAME venue_id
    active_gigs_at_this_venue = Gig.query.filter(Gig.venue_id==gig_fields["venue_id"], Gig.is_expired==False).all()
    # FOR EACH ACTIVE GIG, IF GIG EXISTS WITH A start_time WITHIN 2 HOURS OF THE REQUEST'S start_time, RETURN DESCRIPTIVE ERROR
    for g in active_gigs_at_this_venue:
        delta = g.start_time - gig_fields["start_time"]
        if (g.start_time.date()==gig_fields["start_time"].date()) and (delta.total_seconds() <= 7200) and (delta.total_seconds() >= -7200):
            return abort(409, description=Markup(f"{g.artists} has a gig within 2 hours of this at {g.gig_venue.name} (http://localhost:5000/gigs/{g.id})"))
    # CHECK IF REQUEST start_time IS IN FUTURE
    if gig_fields["start_time"] < datetime.now():
        return abort(409, description=Markup(f"Invalid input - start time must be in the future"))
    # IF ALL GOOD, CREATE A NEW GIG WITH THE REQUEST FIELDS
    gig = Gig(
        title = gig_fields["title"],
        start_time = gig_fields["start_time"],
        date_added = datetime.now(),
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
    # ADD NEW GIG TO SESSION AND COMMIT TO DATABASE
    db.session.add(gig)
    db.session.commit()
    # ITERATE THROUGH
    artist_input = gig.artists.split(", ")
    for artist in artist_input:
        # QUERY ARTISTS TABLE TO CHECK IF EACH ARTIST IN REQUEST ALREADY EXISTS (CASE INSENSITIVE)
        artist_exists = Artist.query.filter(func.lower(Artist.name)==(func.lower(artist))).first()
        if not artist_exists:
            # IF ARTIST DOES NOT ALREADY EXIST IN DATABASE, CREATE NEW ARTIST
            artist = Artist(
                name = artist
            )
            # ADD ARTIST TO SESSION AND COMMIT
            db.session.add(artist)
            db.session.commit()
            # CREATE PERFORMANCE WITH gig_id AND artist_id
            performance = Performance(
                gig_id = gig.id,
                artist_id = artist.id
            )
            # ADD PERFORMANCE TO SESSION AND COMMIT
            db.session.add(performance)
            db.session.commit()
        
        else:
            # IF ARTIST ALREADY EXISTS IN DATABASE, CREATE NEW PERFORMANCE WITH NEW GIG'S gig_id AND ARTIST'S artist_id
            performance = Performance(
                gig_id = gig.id,
                artist_id = artist_exists.id
            )
            # ADD PERFORMANCE TO SESSION AND COMMIT
            db.session.add(performance)
            db.session.commit()  

    return jsonify(gig_schema.dump(gig))


@gigs.route("/<int:gig_id>", methods=["PUT"])
@jwt_required()
def update_gig(gig_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(401, description="Unauthorised - user must be logged in")
    # IF USER IS NOT AN ADMIN, ATTEMPT TO FETCH GIG WITH MATCHING gig_id FROM PATH ARGUMENT AND user_id FROM JWT TOKEN
    if not user.admin:
        gig = Gig.query.filter(Gig.id==gig_id, Gig.user_id==user.id).first()
        if not gig:
            return abort(404, description=Markup(f"User must have created gig to update it"))
    # IF USER IS AN ADMIN, SIMPLY FETCH GIG WITH gig_id
    else:
        # GET GIG 
        gig = Gig.query.get(gig_id)
        if not gig:
            return abort(404, description=Markup(f"No gigs found with ID: {gig.id}"))
    
    # TRY TO LOAD REQUEST DATA THROUGH THE SCHEMA
    try: 
        gig_fields = gig_schema.load(request.json, partial=True)
    # IF INVALID, RETURN A DESCRIPTIVE ERROR
    except ValidationError as err:
        return jsonify(err.messages)
    # GET GIG 
    gig = Gig.query.get(gig_id)
    if not gig:
        return abort(404, description=Markup(f"No gigs found with ID: {gig.id}"))
    # PARSE JSON DATA FROM REQUEST
    request_data = request.get_json()
    fields, new_values = [], []
    # PARSE COLUMNS TO UPDATE FROM THE REQUEST DATA
    for attribute in request_data.keys():
        # IF VALUE IS A VALID ATTRIBUTE OF Gig
        if attribute in vars(Gig):
            old_input = getattr(gig, attribute)
            # SET THE ATTRIBUTE TO THE RELEVANT INPUT DATA
            setattr(gig, attribute, gig_fields[attribute])
            new_values.append(gig_fields[attribute])
            fields.append(attribute)
            if attribute == "artists":
                # CREATE ITERABLE LISTS FROM artists STRING
                old_artists = old_input.split(", ")
                new_artists = gig.artists.split(", ")
                for artist in old_artists:
                    # FETCH ARTISTS THAT WERE ORIGINALLY IN THE "artists" COLUMN FROM DATABASE
                    old_artist = Artist.query.filter_by(name=artist).first()
                    # IF ARTIST HAS BEEN REMOVED FROM GIG, DELETE THE RELATED PERFORMANCE
                    if not artist in new_artists:
                        # FETCH PERFORMANCE WITH MATCHING gig_id & artist_id
                        performance = Performance.query.filter(Performance.artist_id==old_artist.id, Performance.gig_id==gig.id).first()
                        # DELETE RECORD
                        db.session.delete(performance)
                
                for artist in new_artists:
                    # QUERY ARTISTS TABLE TO CHECK IF EACH ARTIST IN REQUEST ALREADY EXISTS (CASE INSENSITIVE)
                    artist_exists = Artist.query.filter(func.lower(Artist.name)==(func.lower(artist))).first()
                    if artist_exists:
                        # IF ARTIST EXISTS, QUERY PERFORMANCE TABLE TO CHECK IF THE ARTIST WAS ALREADY PLAYING AT GIG (IF THERE EXISTS A PERFORMANCE OBJECT ALREADY RELATING THE GIG WITH THE ARTIST)
                        duplicate = Performance.query.filter(Performance.artist_id==artist_exists.id, Performance.gig_id==gig.id).first()
                        if not duplicate:
                            # IF THERE'S NO EXISTING PERFORMANCE, CREATE A NEW ONE
                            performance = Performance(
                            gig_id = gig.id,
                            artist_id = artist_exists.id
                            )
                            # ADD PERFORMANCE TO SESSION AND COMMIT
                            db.session.add(performance)
                            db.session.commit()

                    if not artist_exists:
                        # IF ARTIST DOES NOT ALREADY EXIST IN DATABASE (NEW ARTIST), CREATE NEW ARTIST
                        artist = Artist(
                            name = artist
                        )
                        # ADD ARTIST TO SESSION AND COMMIT
                        db.session.add(artist)
                        db.session.commit()
                        # CREATE PERFORMANCE WITH artist_id AND gig_id
                        performance = Performance(
                            gig_id = gig.id,
                            artist_id = artist.id
                        )
                        # ADD PERFORMANCE TO SESSION AND COMMIT
                        db.session.add(performance)
                        db.session.commit()
    # COMMIT ALL CHANGES TO THE DATABASE
    db.session.commit()

    return jsonify(message=Markup(f"{gig.title}'s {', '.join(str(field) for field in fields)} successfully updated"))
        

@gigs.route("/<int:gig_id>", methods=["DELETE"])
@jwt_required()
def delete_gig(gig_id):
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(int(get_jwt_identity()))
    # FETCH GIG WITH gig_id FROM PATH PARAMETER
    gig = Gig.query.get(gig_id)
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    if not gig:
        return abort(404, description=Markup(f"Gig doesn't exist with that ID"))
    # QUERY GIG TABLE TO CHECK IF GIG WAS CREATED BY CURRENT USER FROM ABOVE QUERY
    user_created_gig = Gig.query.filter(Gig.user_id==user.id, Gig.id==gig_id).first()
    if not user_created_gig:
        return abort(401, description=Markup(f"User didn't create gig"))
    # IF REQUEST IS VALID THEN DELETE GIG FROM DATABASE AND COMMIT
    db.session.delete(gig)
    db.session.commit()

    return jsonify(message=Markup(f"{gig.title} has been deleted"))


@gigs.route("/watchlist", methods=["GET"])
@jwt_required()
def show_watchlist():
    # FETCH USER WITH user_id AS RETURNED BY get_jwt_identity() FROM JWT TOKEN
    user = User.query.get(get_jwt_identity())
    if not user or not user.logged_in:
        return abort(401, description="User not logged in")

    watchlist_schema = UserSchema(only=("username", "watched_venues", "watched_artists"))

    return jsonify(watchlist_schema.dump(user))