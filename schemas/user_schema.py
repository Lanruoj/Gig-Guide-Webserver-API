from main import ma
from marshmallow.validate import Length, ContainsOnly
from marshmallow import fields
from string import ascii_lowercase, ascii_uppercase, digits


alphanumeric = ascii_uppercase + ascii_lowercase + digits


class UserSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("user_id", "username", "email", "password", "first_name", "last_name", "logged_in", "watched_venues", "watched_artists", "gigs")
        load_only = ["password"]

    username = ma.String(required=True, validate=[Length(min=1, max=32), ContainsOnly(alphanumeric + "_")])
    password = ma.String(required=True, validate=Length(min=8))
    email = ma.Email(required=True)
    first_name = ma.String(required=True, validate=[Length(min=1, max=32), ContainsOnly(ascii_uppercase + ascii_lowercase)])
    last_name = ma.String(required=True, validate=[Length(min=1, max=32), ContainsOnly(ascii_uppercase + ascii_lowercase)])

    watched_venues = fields.List(fields.Nested("WatchVenueSchema"))
    watched_artists = fields.List(fields.Nested("WatchArtistSchema"))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
