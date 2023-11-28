from unittest.mock import mock_open, patch

from truth.truth import AssertThat

from freshcart.lib.db import get_every_product, read
from freshcart.lib.models import db
from freshcart.lib.models.products import Product
from freshcart.tests import AppTestCase, DbMixin


class TestDb(DbMixin, AppTestCase):
    def test_read_existing_file_works(self) -> None:
        file_path = "test_module.py"
        file_contents = "print('Hello, world!')\n"

        with patch("builtins.open", mock_open(read_data=file_contents)) as m:
            result = read("test_module")
            AssertThat(m).WasCalled().Once().With(file_path, "r")
            AssertThat(result).IsEqualTo(file_contents)

    def test_read_non_existing_file_handles_error(self) -> None:
        non_existing_file_path = "non_existing_module.py"

        with patch("builtins.open", mock_open()) as m:
            m.side_effect = FileNotFoundError
            result = read("non_existing_module")
            AssertThat(m).WasCalled().Once().With(non_existing_file_path, "r")
            AssertThat(result).IsEqualTo("")

    def test_get_every_product_returns_every_product(self) -> None:
        product_1 = Product(name="Test product 1", price=10.0)
        product_2 = Product(name="Test product 2", price=20.0)
        product_3 = Product(name="Test product 3", price=30.0)

        db.session.add(product_1)
        db.session.add(product_2)
        db.session.add(product_3)
        db.session.commit()

        products = get_every_product()

        AssertThat(products[0]).IsEqualTo(product_1)
        AssertThat(products[1]).IsEqualTo(product_2)
        AssertThat(products[2]).IsEqualTo(product_3)
