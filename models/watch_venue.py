from main import db


class WatchVenue(db.Model):
    __tablename__ = "watch_venues"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)

    venue = db.relationship(
        "Venue",
        back_populates="venue_wv"
    )
