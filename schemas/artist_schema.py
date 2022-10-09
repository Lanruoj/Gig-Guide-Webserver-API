from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class ArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "country_id", "country", "genres", "artist_genres", "performances")

    name = ma.String(required=True, validate=Length(min=1))
    country_id = ma.Integer()
    
    country = fields.Nested("CountrySchema")
    artist_genres = fields.List(fields.Nested("ArtistGenreSchema"))
    performances = fields.List(fields.Nested("PerformanceSchema"))


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)