from main import db


class WatchArtist(db.Model):
    __tablename__ = "watch_artists"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)