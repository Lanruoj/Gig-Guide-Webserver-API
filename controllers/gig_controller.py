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
        user_id = get_jwt_identity()
    )
    db.session.add(gig)
    db.session.commit()

    return jsonify(gig_schema.dump(gig))


@gigs.route("/<int:gig_id>/performance", methods=["POST"])
def add_performance(gig_id):
    performance_fields = performance_schema.load(request.json)
    performance = Performance(
        gig_id = gig_id,
        artist_id = performance_fields["artist_id"]
    )
    db.session.add(performance)
    db.session.commit()

    return jsonify(performance_schema.dump(performance))