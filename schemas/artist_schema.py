from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class ArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "genre", "country_id", "country", "performances")
        load_only = ["country_id"]

    name = ma.String(required=True, validate=Length(min=1))
    genre = ma.String()

    country = fields.Nested("CountrySchema")
    performances = fields.List(fields.Nested("PerformanceSchema"))


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)