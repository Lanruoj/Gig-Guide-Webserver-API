from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class CountrySchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")

    name = ma.String(required=True, validate=Length(min=1))
    genre = ma.String()

    performances = fields.List(fields.Nested("PerformanceSchema"))


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)