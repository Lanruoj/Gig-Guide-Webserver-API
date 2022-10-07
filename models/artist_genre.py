from main import db


class ArtistGenre(db.Model):
    __tablename__ = "artist_genres"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), nullable=False)

    ag_artist = db.relationship(
        "Artist",
        back_populates="genres"
    )

    ag_genre = db.relationship(
        "Genre",
        back_populates="genre_ag"
    )