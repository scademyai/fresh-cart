from . import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name} price={self.price})>"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }
