from photo_backend.extensions import db


class Action(db.Model):
    __tablename__ = "action"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    images = db.relationship("Image",
                             backref="action",
                             cascade="delete")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "images": [img.to_dict() for img in self.images]}


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    description = db.Column(db.String(128), nullable=False)
    action_id = db.Column(db.ForeignKey(
        Action.id, ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "link": self.link, "description": self.description}


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    message = db.Column(db.String(512), nullable=False)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "subject": self.subject, "message": self.message}
