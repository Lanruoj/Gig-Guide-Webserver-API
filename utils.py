from flask import request, abort, jsonify, Markup
from sqlalchemy import desc


def search(table, schema, filters=None, sort=None, asc=True, no_results="No results found"):
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