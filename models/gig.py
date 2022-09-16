from main import db


class Gig(db.Model):
    __tablename__ = "gigs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), default="N/A")
    start_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime)
    artists = db.Column(db.String(), nullable=False)
    
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    venue = db.relationship(
        "Venue",
        backref="gig_venue"
    )
    
    performances = db.relationship(
        "Performance",
        backref="g_gig"
    )