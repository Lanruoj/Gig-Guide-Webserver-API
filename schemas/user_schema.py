from main import ma
from marshmallow.validate import Length


class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "username", "email", "password", "first_name", "last_name")
    password = ma.String(validate=Length(min=8))
    username = ma.String(required=True)
    email = ma.String(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
