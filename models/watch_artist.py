from main import db


class WatchArtist(db.Model):
    __tablename__ = "watch_artists"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)

    artist = db.relationship(
        "Artist",
        back_populates="artist_wa"
    )