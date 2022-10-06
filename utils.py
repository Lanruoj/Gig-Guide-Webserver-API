from flask import request, abort, jsonify, Markup
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from marshmallow.exceptions import ValidationError


def search_table(table, filters=None, sort=None, asc=True, no_results="No results found"):
    # IF NO FILTERS GIVEN/PASSED WHEN FUNCTION IS CALLED, ASSIGN THEM WITHIN THE FUNCTION
    if not filters:
        filters = []
    # CHECK IF THERE ARE ARGUMENTS IN THE QUERY STRING
    if request.query_string:
        no_results = "No results matching that criteria"
        # ITERATE THROUGH ARGUMENTS IN QUERY STRING
        for arg in request.args:
            # VALIDATE WHETHER ARGUMENT IN QUERY STRING IS VALID
            if (arg not in vars(table)) and (arg != "sort:asc") and (arg != "sort:desc"):
                return abort(400, description=Markup(f"The keyword '{arg}' is not valid search criteria"))
            # CHECK FOR A SORT ARGUMENT
            elif arg == "sort:asc":
                # IF sort:asc IS FOUND THEN LEAVE asc=True & desc=False (DEFAULTS)
                sort = getattr(table, request.args[arg])
                asc = True

            elif arg == "sort:desc":
                # IF sort:desc IS FOUND THEN SET asc=False & desc=True
                sort = getattr(table, request.args[arg])
                asc = False
            # IF NOT A SORTING ARGUMENT, THEN IT IS AN ATTRIBUTE QUERY
            else:
                # IF SEARCHING FOR A NUMERIC VALUE, MATCH VALUE EXACTLY
                if "id" in arg or request.args[arg].isdigit():
                    _filter = getattr(table, arg) == request.args[arg]
                    filters.append(_filter)
                # IF SEARCHING FOR A STRING VALUE, PERFORM A CASE INSENSITIVE STRING MATCH QUERY
                else:
                    _filter = getattr(table, arg).ilike(f"%{request.args[arg]}%")
                    filters.append(_filter)
    # SORT BY DESCENDING ORDER
    if not asc:
        results = table.query.filter(*(filters)).order_by(desc(sort)).all()
    # SORT BY ASCENDING ORDER
    elif asc:
        results = table.query.filter(*(filters)).order_by(sort).all()

    if not results:
        return abort(404, description=no_results)

    return results


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

    return record