from main import ma
from marshmallow import fields


class PerformanceSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "gig_id", "artist_id", "artist")
    artist = fields.Nested("ArtistSchema", only=("name",))


performance_schema = PerformanceSchema()
performances_schema = PerformanceSchema(many=True)