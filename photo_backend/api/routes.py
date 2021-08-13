from flask import Blueprint, jsonify, request

from .models import Image

from photo_backend.extensions import db
from photo_backend.utils import token_required

blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.get("/images")
def get_all_images():
    return jsonify([img.to_dict() for img in Image.query.all()]), 200

@blueprint.post("/image")
@token_required
def add_image():
    img = Image(link=request.json["link"],
                description=request.json["description"])
    db.session.add(img)
    db.session.commit()
    return jsonify({"message": "Added succesfully"}), 201

@blueprint.get("/image/<int:id>")
def get_one_image(id):
    return jsonify(Image.query.get_or_404(id).to_dict()), 200

@blueprint.delete("/image/<int:id>")
@token_required
def remove_image(id):
    img = Image.query.get_or_404(id)
    db.session.delete(img)
    db.session.commit()
    return jsonify({"message":"Deleted succesfully"})
