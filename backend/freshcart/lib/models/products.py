from pgvector.sqlalchemy import Vector
from sqlalchemy import select, text
from sqlalchemy.orm import object_session

from . import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    embedding = db.Column(Vector(1536), nullable=True)

    @property
    def similar(self):
        if self.embedding is None:
            return []

        # EXERCISE 6. - Similar products
        # You task is to write the query for similar products.
        # Use embedding to find similar products list them by similarity.
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # SELECT p.id, p.name, p.price FROM products p
        # WHERE p.id != :product_id
        # ORDER BY <embedding> ASC LIMIT 15;

        sql = text(
            """
            SELECT p.id, p.name, p.price FROM products p 
            WHERE p.id != :product_id 
            ORDER BY p.embedding <#> :embedding ASC LIMIT 15;
        """
        ).columns(Product.id, Product.name, Product.price)

        if not (session := object_session(self)):
            return []

        return session.scalars(
            select(Product).from_statement(sql),
            {"product_id": self.id, "embedding": self.embedding},
        ).all()

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name} price={self.price})>"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }
