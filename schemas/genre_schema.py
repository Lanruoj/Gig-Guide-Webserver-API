from main import ma
from marshmallow import fields
from marshmallow.validate import Length


class GenreSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)