from main import ma
from marshmallow import fields


class ArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "genre", "performances", "gigs")

    performances = fields.List(fields.Nested("PerformanceSchema"))
    # gigs = fields.List(fields.Nested("GigSchema", only=("title",)))


artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)