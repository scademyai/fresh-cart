from pgvector.sqlalchemy import Vector

from . import db


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    embedding = db.Column(Vector(1536), nullable=True)

    def __repr__(self):
        return f"<Document(id={self.id}), content={self.content}>"
