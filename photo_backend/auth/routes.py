import os
import jwt
from flask import Blueprint, request, jsonify

from photo_backend.extensions import bcrypt, db
from photo_backend.utils import token_required

from .models import User

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.post("/register")
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User(email, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "success"}), 201


@blueprint.post("/login")
def login_user():
    email = request.json["email"]
    password = request.json["password"]
    user = User.query.get_or_404(email)

    if bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({
            "email": email,
            "password": password,
            "version": user.jwt_version
        }, os.getenv("JWT_SECRET"))
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid login"}), 401


@blueprint.get("/me")
@token_required
def get_user():
    email = request.json["email"]
    user = User.query.get_or_404(email)
    return jsonify({"email": email, "token_version": user.jwt_version}), 200
