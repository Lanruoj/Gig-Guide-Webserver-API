from main import ma
from marshmallow import fields


class ArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "genre")
    # performances = fields.List(fields.Nested("PerformanceSchema"))


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)