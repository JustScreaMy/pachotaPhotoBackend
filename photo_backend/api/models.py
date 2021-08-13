from photo_backend.extensions import db


class Action(db.Model):
    __tablename__ = "action"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    description = db.Column(db.String(128))
    action_id = db.Column(db.ForeignKey(Action.id))
    action = db.relationship("Action")

    def to_dict(self):
        return {"id": self.id, "link": self.link, "description": self.description, "action": self.action.name}
