from main import ma


class VenueTypeSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name")


venue_type_schema = VenueTypeSchema()
venue_types_schema = VenueTypeSchema(many=True)