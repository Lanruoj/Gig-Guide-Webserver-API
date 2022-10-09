from main import ma


class GenreSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)