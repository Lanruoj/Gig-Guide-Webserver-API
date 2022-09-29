from main import ma
from marshmallow import fields


class WatchArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "user_id", "artist_id", "artist")
    
    user_id = ma.Integer(required=True)
    artist_id = ma.Integer(required=True)
    
    artist = fields.Nested("ArtistSchema")


watch_artist_schema = WatchArtistSchema()
watch_artists_schema = WatchArtistSchema(many=True)