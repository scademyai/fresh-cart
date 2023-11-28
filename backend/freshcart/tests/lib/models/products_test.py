import unittest

from truth.truth import AssertThat

from freshcart.lib.models.products import Product


class TestProducts(unittest.TestCase):
    def test_json_returns_formatted_products(self) -> None:
        product = Product(id=1, name="Test Product", price=100)

        AssertThat(product.json()).IsEqualTo(
            {
                "id": 1,
                "name": "Test Product",
                "price": 100,
            }
        )
