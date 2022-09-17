from main import ma
from marshmallow import fields


class PerformanceSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "gig_id", "artist_id", "artist", "gig")
        # load_only = ["id", "gig_id", "artist", "artist_id"]
    artist = fields.Nested("ArtistSchema", only=("name",))
    gig = fields.Nested("GigSchema")


performance_schema = PerformanceSchema()
performances_schema = PerformanceSchema(many=True)