from main import ma
from marshmallow import fields

class WatchVenueSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "user_id", "venue_id", "venue")
    
    venue = fields.Nested("VenueSchema")
    

watch_venue_schema = WatchVenueSchema()
watch_venues_schema = WatchVenueSchema(many=True)