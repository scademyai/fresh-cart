import jwt
from truth.truth import AssertThat

from freshcart.lib.models import db
from freshcart.lib.models.products import Product
from freshcart.lib.models.sessions import Session

from . import AppTestCase, DbMixin, TestClientMixin


class TestAppHttp(TestClientMixin, DbMixin, AppTestCase):
    def test_products_endpoint_returns_200(self):
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}
        r = self.client.get("/products", headers=headers)

        AssertThat(r.status_code).IsEqualTo(200)

    def test_products_endpoint_returns_every_product(self):
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}

        product = Product(name="test", price=10)
        db.session.add(product)
        db.session.commit()

        r = self.client.get("/products", headers=headers)

        AssertThat(r.json[0]["id"]).IsEqualTo(product.id)
        AssertThat(r.json[0]["name"]).IsEqualTo(product.name)
        AssertThat(r.json[0]["price"]).IsEqualTo(product.price)

    def test_get_product_endpoint_returns_200(self):
        anchor_product = Product(
            name="test", price=10, embedding=[1] + [0] * 1535
        )
        for i in range(15):
            db.session.add(
                Product(
                    name=f"test_similar_{i}",
                    price=i * 5,
                    embedding=[1 - i * 0.01] + [0] * 1534 + [i * 0.01],
                )
            )

        dissimilar_product = Product(
            name="test_dissimilar", price=10, embedding=[0] * 1535 + [1]
        )

        db.session.add(anchor_product)
        db.session.add(dissimilar_product)
        db.session.commit()
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}
        r = self.client.get(f"/products/{anchor_product.id}", headers=headers)

        AssertThat(r.status_code).IsEqualTo(200)

        AssertThat([p["name"] for p in r.json["similar"]]).DoesNotContain(
            "test_dissimilar"
        )

    def test_refresh_session_endpoint_refreshes_session_id(self) -> None:
        r = self.client.get("/refresh-session")
        token = r.json["access_token"]

        r2 = self.client.get("/refresh-session")

        AssertThat(r2.json["access_token"]).IsNotEqualTo(token)

    def test_refresh_session_endpoint_saves_session_id(self) -> None:
        r = self.client.get("/refresh-session")

        session_id = jwt.decode(
            r.json["access_token"], self.app.secret_key, algorithms=["HS256"]
        )["sub"]
        db_session = Session.query.first()

        AssertThat(str(db_session.id)).IsEqualTo(session_id)

    def test_refresh_session_endpoint_returns_200_token(self) -> None:
        r = self.client.get("/refresh-session")

        AssertThat(r.status_code).IsEqualTo(200)
        AssertThat(r.json["access_token"]).IsNotNone()

    def test_cart_returns_cart_contents(self) -> None:
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}

        self.client.post(
            "/cart",
            json={"product": {"id": 1, "quantity": 1}},
            headers=headers,
        )

        r = self.client.get("/cart", headers=headers)

        AssertThat(r.json["cart"]).IsEqualTo([{"id": 1, "quantity": 1}])

    def test_cart_saves_new_cart_contents(self) -> None:
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}

        self.client.post(
            "/cart",
            json={"product": {"id": 1, "quantity": 1}},
            headers=headers,
        )

        session_id = jwt.decode(
            r.json["access_token"], self.app.secret_key, algorithms=["HS256"]
        )["sub"]
        session_from_db = Session.query.get(session_id)

        AssertThat(session_from_db.cart).IsEqualTo([{"id": 1, "quantity": 1}])

    def test_cart_returns_updated_cart(self) -> None:
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}

        r = self.client.post(
            "/cart",
            json={"product": {"id": 1, "quantity": 1}},
            headers=headers,
        )

        AssertThat(r.json["cart"]).IsEqualTo([{"id": 1, "quantity": 1}])

    def test_delete_cart_returns_empty_cart(self) -> None:
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}

        db_session = Session.query.first()
        db_session.cart = [{"id": 1, "quantity": 1}]
        db.session.add(db_session)
        db.session.commit()

        r = self.client.delete("/cart", headers=headers)

        AssertThat(r.json["cart"]).IsEqualTo([])

    def test_remove_from_cart_removes_item_from_cart(self) -> None:
        r = self.client.get("/refresh-session")
        headers = {"Authorization": f"Bearer {r.json['access_token']}"}

        db_session = Session.query.first()
        db_session.cart = [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 3}]
        db.session.add(db_session)
        db.session.commit()

        r = self.client.delete("/cart/1", headers=headers)

        AssertThat(r.json["cart"]).IsEqualTo([{"id": 2, "quantity": 3}])
