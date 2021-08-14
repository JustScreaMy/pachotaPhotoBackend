from photo_backend.extensions import db


class Action(db.Model):
    __tablename__ = "action"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    images = db.relationship("Image",
                             backref="action")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "images": [img.to_dict() for img in self.images]}


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    description = db.Column(db.String(128))
    action_id = db.Column(db.ForeignKey(Action.id))

    def to_dict(self):
        return {"id": self.id, "link": self.link, "description": self.description}
