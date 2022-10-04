from flask import request, abort, jsonify, Markup
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from marshmallow.exceptions import ValidationError


def search_table(table, schema, filters=None, sort=None, asc=True, no_results="No results found"):
    if not filters:
        filters = []
    if request.query_string:
        no_results = "No results matching that criteria"
        for arg in request.args:
            if arg not in vars(table) and arg != "sort:asc" and arg != "sort:desc":
                return abort(400, description=Markup(f"The keyword '{arg}' is not valid search criteria"))

            if arg == "sort:asc":
                sort = getattr(table, request.args[arg])
                asc = True

            elif arg == "sort:desc":
                sort = getattr(table, request.args[arg])
                asc = False

            elif arg != "sort":
                # IF SEARCHING FOR A NUMERIC VALUE
                if "id" in arg or request.args[arg].isdigit():
                    _filter = getattr(table, arg) == request.args[arg]
                    filters.append(_filter)
                # IF SEARCHING FOR A STRING VALUE
                else:
                    _filter = getattr(table, arg).ilike(f"%{request.args[arg]}%")
                    filters.append(_filter)

    if not asc:
        results = table.query.filter(*(filters)).order_by(desc(sort)).all()
    else:
        results = table.query.filter(*(filters)).order_by(sort).all()

    if not results:
        return abort(404, description=no_results)

    return jsonify(schema.dump(results))


def update_record(record_id, table, schema):
    try: 
        schema_fields = schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages)
    
    record = table.query.get(record_id)
    if not record:
        return abort(404, description=Markup(f"{table.__name__} does not exist"))
    
    request_data = request.get_json()

    fields, new_values = [], []
    for attribute in request_data.keys():
        if attribute in vars(table):
            setattr(record, attribute, schema_fields[attribute])
            new_values.append(schema_fields[attribute])
            fields.append(attribute)

    return jsonify(message=Markup(f"{record.name}'s {', '.join(str(field) for field in fields)} successfully updated to {', '.join(str(value) for value in new_values)}"))