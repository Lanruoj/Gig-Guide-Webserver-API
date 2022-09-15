from main import db, bcrypt, jwt
from flask import Blueprint, jsonify, request, abort
from models.gig import Gig
from schemas.gig_schema import gig_schema, gigs_schema


gigs = Blueprint("gigs", __name__, url_prefix="/gigs")


@gigs.route("/", methods=["GET"])
def show_all_gigs():
    # SELECT ALL RECORDS FROM THE gigs TABLE. IF NO RECORDS, RETURN DESCRIPTIVE MESSAGE
    gigs_list = Gig.query.all()

    if not gigs_list:
        return jsonify(message="Currently no gigs")

    return jsonify(gig_schema.dump(gigs_list))