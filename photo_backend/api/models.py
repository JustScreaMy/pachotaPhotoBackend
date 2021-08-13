from photo_backend.extensions import db


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    description = db.Column(db.String(64))

    def to_dict(self):
        return {"id": self.id, "link": self.link, "description": self.description}
