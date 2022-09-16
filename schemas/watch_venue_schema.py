from main import ma


class WatchVenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "user_id", "venue_id")
    

watch_venue_schema = WatchVenueSchema()
watch_venues_schema = WatchVenueSchema(many=True)