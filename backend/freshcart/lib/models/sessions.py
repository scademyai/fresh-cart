from sqlalchemy.dialects.postgresql import UUID

from . import db


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    cart = db.Column(db.JSON)

    def __repr__(self):
        return f"<Session(id={self.id}, cart={self.cart})>"
