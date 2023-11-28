from unittest.mock import patch

from sqlalchemy import func
from truth.truth import AssertThat

from freshcart.lib.embedder import embed_product
from freshcart.lib.models import db
from freshcart.lib.models.products import Product
from freshcart.tests import AppTestCase, DbMixin


class TestEmbedder(DbMixin, AppTestCase):
    def test_embedder_product_does_not_exist(self):
        embed_product(1)

        AssertThat(
            db.session.query(func.count(Product.id)).scalar()
        ).IsEqualTo(0)

    def test_embedder_product_already_embedded(self):
        embedding = embedding = [1] * 1536
        product = Product(name="test", embedding=embedding)
        db.session.add(product)
        db.session.commit()

        embed_product(product.id)

        AssertThat(
            Product.query.get(product.id).embedding
        ).ContainsExactlyElementsIn(embedding).InOrder()

    @patch("freshcart.lib.embedder.embed_text", return_value=[2] * 1536)
    def test_embedder_product_not_embedded(self, _):
        product = Product(name="test")
        db.session.add(product)
        db.session.commit()

        embed_product(product.id)

        AssertThat(
            Product.query.get(product.id).embedding
        ).ContainsExactlyElementsIn([2] * 1536).InOrder()
