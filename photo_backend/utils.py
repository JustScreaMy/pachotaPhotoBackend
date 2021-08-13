import os
from functools import wraps

import jwt
from flask import request
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
        