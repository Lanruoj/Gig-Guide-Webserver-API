from flask import request, abort, jsonify, Markup


def search(table, schema, filters=None, sort=None, no_results="No results found"):
    if not filters:
        filters = []
    if request.query_string:
        no_results = "No results matching that criteria"
        for arg in request.args:
            if arg not in vars(table) and arg != "sort":
                return abort(400, description=Markup(f"The keyword '{arg}' is not valid search criteria"))

            if arg == "sort":
                sort = getattr(table, request.args[arg])

            elif arg != "sort":
                # IF SEARCHING FOR A NUMERIC VALUE
                if "id" in arg or request.args[arg].isdigit():
                    _filter = getattr(table, arg) == request.args[arg]
                    filters.append(_filter)
                # IF SEARCHING FOR A STRING VALUE
                else:
                    _filter = getattr(table, arg).ilike(f"%{request.args[arg]}%")
                    filters.append(_filter)


    results = table.query.filter(*(filters)).order_by(sort).all()
    if not results:
        return abort(404, description=no_results)

    return jsonify(schema.dump(results))