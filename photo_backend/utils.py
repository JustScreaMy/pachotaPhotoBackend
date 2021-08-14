import os
import re
from functools import wraps

import jwt
from flask import request, jsonify
from flask.wrappers import Response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return Response(status=401)
        try:
            data = jwt.decode(token, os.getenv(
                "JWT_SECRET"), algorithms=["HS256"])
        except:
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated


def required_params(*args):
    required = list(args)

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            missing = [r for r in required if r not in request.get_json()]
            if missing:
                response = {
                    "message": f"Missing {', '.join(missing)}",
                }
                return jsonify(response), 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def parse_db_uri(uri: str):
    if re.search("postgres", uri):
        return uri.replace("postgres", "postgresql+psycopg2")
    return uri
