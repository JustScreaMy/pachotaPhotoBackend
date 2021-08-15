import re
from flask import Blueprint, jsonify, request

from photo_backend.extensions import db
from photo_backend.utils import token_required, required_params

from .models import Action, Feedback, Image

blueprint = Blueprint("api", __name__, url_prefix="/api")

"""
====================
IMAGES
====================
"""


@blueprint.post("/image")
@token_required
@required_params("link", "description", "action_id")
def add_image():
    if not Action.query.get(request.json["action_id"]):
        return jsonify({"message": "Invalid action!"}), 400
    img = Image(link=request.json["link"],
                description=request.json["description"],
                action_id=request.json["action_id"])
    db.session.add(img)
    db.session.commit()
    return jsonify({"message": "Added succesfully"}), 201


@blueprint.delete("/image/<int:id>")
@token_required
def remove_image(id):
    img = Image.query.get_or_404(id)
    db.session.delete(img)
    db.session.commit()
    return jsonify({"message": "Deleted succesfully"}), 200


@blueprint.get("/images")
def get_all_images():
    return jsonify([img.to_dict() for img in Image.query.all()]), 200


@blueprint.get("/image/<int:id>")
def get_one_image(id):
    return jsonify(Image.query.get_or_404(id).to_dict()), 200


"""
====================
ACTIONS
====================
"""


@blueprint.post("/action")
@token_required
@required_params("name", "images")
def add_action():

    action = Action(name=request.json["name"])
    db.session.add(action)
    db.session.commit()

    images = [
        Image(link=img["link"],
              description=img["description"],
              action_id=action.id)
        for img in request.json["images"]
    ]

    db.session.add_all(images)
    db.session.commit()

    return jsonify({"message": "Added succesfully"}), 201


@blueprint.delete("/action/<int:id>")
@token_required
def remove_action(id):
    action = Action.query.get_or_404(id)
    db.session.delete(action)
    db.session.commit()
    return jsonify({"message": "Deleted succesfully"}), 200


@blueprint.get("/actions")
def get_all_actions():
    return jsonify([action.to_dict() for action in Action.query.all()]), 200


@blueprint.get("/action/<int:id>")
def get_action(id):
    return jsonify(Action.query.get_or_404(id).to_dict()), 200


"""
====================
Feedback
====================
"""


@blueprint.post("/feedback")
@required_params("email", "subject", "message")
def add_feedback():
    feedback = Feedback(
        email=request.json["email"],
        subject=request.json["subject"],
        message=request.json["message"],
    )

    db.session.add(feedback)
    db.session.commit()

    return jsonify({"message": "Added succesfully"}), 201


@blueprint.delete("/feedback/<int:id>")
@token_required
def delete_feedback():
    feedback = Feedback.query.get_or_404(id)

    db.session.delete(feedback)
    db.session.commit()

    return jsonify({"message": "Deleted succesfully"}), 200


@blueprint.get("/feedbacks")
def get_feedbacks():
    return jsonify([feedback.to_dict() for feedback in Feedback.query.all()]), 200
