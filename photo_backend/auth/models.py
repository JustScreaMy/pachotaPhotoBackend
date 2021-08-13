from photo_backend.extensions import bcrypt, db


class User(db.Model):
    """A user of the app."""

    __tablename__ = "users"
    email = db.Column(
        db.String(80),
        primary_key=True,
    )
    password = db.Column(db.LargeBinary(128), nullable=False)
    jwt_version = db.Column(db.Integer)

    def __init__(self, email, password=None, jwt_version=1, **kwargs):
        """Create instance."""
        self.email = email
        self.set_password(password)
        self.jwt_version = jwt_version

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.email!r})>"
