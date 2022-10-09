from main import ma
from marshmallow import fields
from schemas.genre_schema import GenreSchema


class ArtistGenreSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "artist_id", "genre_id", "ag_genre")

    artist_id = ma.Integer(required=True)
    genre_id = ma.Integer(required=True)
    
    ag_genre = fields.Nested(GenreSchema)


artist_genre_schema = ArtistGenreSchema()
artist_genres_schema = ArtistGenreSchema(many=True)