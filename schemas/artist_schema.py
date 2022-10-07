from main import ma
from marshmallow import fields
from marshmallow.validate import Length
from schemas.artist_genre_schema import ArtistGenreSchema


class ArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "country_id", "country", "genres", "artist_genres", "performances")
        # load_only = ["country_id"]

    name = ma.String(required=True, validate=Length(min=1))

    artist_genres = fields.List(fields.Nested("ArtistGenreSchema"))

    country = fields.Nested("CountrySchema")
    performances = fields.List(fields.Nested("PerformanceSchema"))


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)