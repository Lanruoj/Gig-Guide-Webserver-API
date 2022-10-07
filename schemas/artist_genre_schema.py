from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class ArtistGenreSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "artist_id", "genre_id")


artist_genre_schema = ArtistGenreSchema()
artist_genres_schema = ArtistGenreSchema(many=True)