from main import ma
from marshmallow.validate import Length
from marshmallow import fields


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("user_id", "username", "email", "password", "first_name", "last_name", "logged_in", "watched_venues", "watched_artists")
    
    username = ma.String(required=True, validate=Length(min=3, max=10))
    password = ma.String(required=True, validate=Length(min=8))
    email = ma.Email(required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)

    watched_venues = fields.List(fields.Nested("WatchVenueSchema"))
    watched_artists = fields.List(fields.Nested("WatchArtistSchema"))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
