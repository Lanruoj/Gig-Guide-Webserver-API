from flask import request, abort, jsonify


def search(table, schema, filters=None, sort=None, no_results="No results found"):
    if not filters:
        filters = []
        
    if request.query_string:
        no_results = "No results matching that criteria"
        for arg in request.args:
            if arg != "sort":
                if "id" in arg:
                    _filter = getattr(table, arg) == request.args[arg]
                    filters.append(_filter)
                else:
                    _filter = getattr(table, arg).ilike(f"%{request.args[arg]}%")
                    filters.append(_filter)

            elif arg == "sort":
                sort = getattr(table, request.args[arg])

    results = table.query.filter(*(filters)).order_by(sort).all()
    if not results:
        return abort(404, description=no_results)

    return jsonify(schema.dump(results))