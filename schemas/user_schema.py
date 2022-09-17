from main import ma
from marshmallow.validate import Length
from marshmallow import fields


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "email", "password", "first_name", "last_name", "watched_venues")
    password = ma.String(validate=Length(min=8))
    username = ma.String(required=True)
    email = ma.String(required=True)

    #######
    watched_venues = fields.List(fields.Nested("WatchVenueSchema"))


user_schema = UserSchema()
users_schema = UserSchema(many=True)
