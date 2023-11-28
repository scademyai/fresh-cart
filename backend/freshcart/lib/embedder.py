from .ai.llm_adapter import embed_text
from .models import db
from .models.products import Product


def embed_product(product_id: int):
    product = Product.query.get(product_id)
    if product is None or product.embedding is not None:
        return

    embedding = embed_text(product.name)
    product.embedding = embedding
    db.session.commit()
