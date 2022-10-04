from main import db
from datetime import timedelta, datetime


class Gig(db.Model):
    __tablename__ = "gigs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), default="N/A")
    artists = db.Column(db.String(), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, default=0)
    tickets_url = db.Column(db.String(), default="N/A")
    timestamp = db.Column(db.DateTime)
    # is_deleted = db.Column(db.Boolean, default=False)
    is_expired = db.Column(db.Boolean, default=False)
    
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    venue = db.relationship(
        "Venue",
        backref="gig_venue"
    )

    user = db.relationship(
        "User",
        backref="gig_user"
    )
    
    performances = db.relationship(
        "Performance",
        backref="g_gig"
    )