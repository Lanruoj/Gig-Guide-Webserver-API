from main import ma


class WatchArtistSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "user_id", "artist_id")


watch_artist_schema = WatchArtistSchema()
watch_artists_schema = WatchArtistSchema(many=True)