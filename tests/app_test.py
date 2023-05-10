from unittest.mock import patch

import jwt
from flask_jwt_extended import create_access_token
from flask_socketio import SocketIOTestClient
from truth.truth import AssertThat

from lib.models import db
from lib.models.products import Product
from lib.models.sessions import Session
from tests import AppTestCase, DbMixin, TestClientMixin


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

    def xtest_root_returns_index_html(self) -> None:
        r = self.client.get("/")

        AssertThat(r.status_code).IsEqualTo(200)
        AssertThat(r.headers[0][1]).Contains("index.html")

    def xtest_random_path_index_html(self) -> None:
        r = self.client.get("/non-existing-path")

        AssertThat(r.status_code).IsEqualTo(200)
        AssertThat(r.headers[0][1]).Contains("index.html")

    def test_app_returns_cors_headers(self) -> None:
        r = self.client.get("/login")

        AssertThat(r.headers.get("Access-Control-Allow-Origin")).IsEqualTo(
            "http://localhost:4200"
        )


class TestAppWebSocket(TestClientMixin, DbMixin, AppTestCase):
    def setUp(self):
        super().setUp()
        self.test_socket = SocketIOTestClient(
            self.app, self.socket, namespace=None
        )

    @patch("app.text_recipe_response")
    def test_simple_recipe_endpoint_works(self, recipe_mock) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("This is a")
            yield test_content("test recipe")

        recipe_mock.return_value = test_generator()

        self.test_socket.emit("simple-recipe", {"text": "test"})
        received = self.test_socket.get_received()

        AssertThat(received[0]["name"]).IsEqualTo("simple-recipe")
        AssertThat(received[0]["args"][0]["text"]).IsEqualTo("This is a")
        AssertThat(received[1]["name"]).IsEqualTo("simple-recipe")
        AssertThat(received[1]["args"][0]["text"]).IsEqualTo("test recipe")

    @patch("app.freshbot_stream")
    def test_messaging_endpoint_works(self, freshbot_mock) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("This is a")
            yield test_content("test message")

        freshbot_mock.return_value = test_generator()

        self.test_socket.emit("freshbot", {"text": "test"})
        received = self.test_socket.get_received()

        AssertThat(received[0]["name"]).IsEqualTo("freshbot")
        AssertThat(received[0]["args"][0]["text"]).IsEqualTo("This is a")
        AssertThat(received[1]["name"]).IsEqualTo("freshbot")
        AssertThat(received[1]["args"][0]["text"]).IsEqualTo("test message")

    @patch("app.json_recipe_response")
    def test_json_recipe_endpoint_works(self, recipe_mock) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content('{"name": "Bacon", "quantity": "1"}')
            yield test_content('{"name": "Eggs", "quantity": "2"}')

        recipe_mock.return_value = test_generator()

        self.test_socket.emit("json-recipe", {"text": "test"})
        received = self.test_socket.get_received()

        AssertThat(received[0]["name"]).IsEqualTo("json-recipe")
        AssertThat(received[0]["args"][0]["json"]).IsEqualTo(
            '{"name": "Bacon", "quantity": "1"}'
        )
        AssertThat(received[1]["name"]).IsEqualTo("json-recipe")
        AssertThat(received[1]["args"][0]["json"]).IsEqualTo(
            '{"name": "Eggs", "quantity": "2"}'
        )

    @patch("app.freshbot_stream")
    @patch("app.categorize_question")
    def test_orchestrate_endpoint_returns_chatbot_answer(
        self, categorize_mock, freshbot_mock
    ) -> None:
        r = self.client.get("/refresh-session")

        def test_fn():
            yield {"choices": [{"delta": {"content": "Website about stuff"}}]}

        categorize_mock.return_value = "website"
        freshbot_mock.return_value = test_fn()

        self.test_socket.emit(
            "orchestrate", {"text": "test", "token": r.json["access_token"]}
        )
        received = self.test_socket.get_received()

        AssertThat(freshbot_mock).WasCalled().Once().With("test")
        AssertThat(received[0]["name"]).IsEqualTo("orchestrate")
        AssertThat(received[0]["args"][0]["text"]).IsEqualTo(
            "Website about stuff"
        )

    @patch("app.cart_query_response")
    @patch("app.categorize_question")
    def test_orchestrate_endpoint_returns_cart_answer(
        self, categorize_mock, cart_mock
    ) -> None:
        r = self.client.get("/refresh-session")
        session_id = jwt.decode(
            r.json["access_token"], self.app.secret_key, algorithms=["HS256"]
        )["sub"]

        def test_fn():
            yield {
                "choices": [{"delta": {"content": "Your cart is expensive"}}]
            }

        categorize_mock.return_value = "cart"
        cart_mock.return_value = test_fn()

        self.test_socket.emit(
            "orchestrate", {"text": "test", "token": r.json["access_token"]}
        )
        received = self.test_socket.get_received()

        AssertThat(cart_mock).WasCalled().Once().With(session_id, "test")
        AssertThat(received[0]["name"]).IsEqualTo("orchestrate")
        AssertThat(received[0]["args"][0]["text"]).IsEqualTo(
            "Your cart is expensive"
        )

    @patch("app.json_recipe_from_product_catalog")
    def test_json_product_catalog_recipe_socket_works(
        self, recipe_text_mock
    ) -> None:
        recipe_text_mock.return_value = []

        self.test_socket.emit("json-product-catalog-recipe", {"text": "test"})
        received = self.test_socket.get_received()

        AssertThat(received[0]["name"]).IsEqualTo(
            "json-product-catalog-recipe"
        )
        AssertThat(received[0]["args"][0]).IsEqualTo([])

    @patch("app.json_recipe_response")
    @patch("app.categorize_question")
    def test_orchestrate_endpoint_returns_recipe_answer(
        self, categorize_mock, recipe_mock
    ) -> None:
        r = self.client.get("/refresh-session")

        def test_fn():
            yield {
                "choices": [
                    {"delta": {"content": '{"name": "Recipe about stuff"}'}}
                ]
            }

        categorize_mock.return_value = "general"
        recipe_mock.return_value = test_fn()

        self.test_socket.emit(
            "orchestrate", {"text": "test", "token": r.json["access_token"]}
        )
        received = self.test_socket.get_received()

        AssertThat(recipe_mock).WasCalled().Once().With("test")
        AssertThat(received[0]["name"]).IsEqualTo("orchestrate")
        AssertThat(received[0]["args"][0]["json"]).IsEqualTo(
            '{"name": "Recipe about stuff"}'
        )

    @patch("app.json_recipe_response")
    def test_orchestrate_endpoint_retries_categorization(
        self, mock_json_recipe
    ) -> None:
        r = self.client.get("/refresh-session")

        def test_fn():
            yield {"choices": [{"delta": {"content": '{"A json": "recipe"}'}}]}

        mock_json_recipe.return_value = test_fn()

        def mock_categorize_function(message):
            mock_categorize_function.call_count += 1
            call_count = mock_categorize_function.call_count

            if call_count == 1:
                return "not_website"
            if call_count == 2:
                return "not_general"
            else:
                return "general"

        mock_categorize_function.call_count = 0

        with patch(
            "app.categorize_question", side_effect=mock_categorize_function
        ):
            self.test_socket.emit(
                "orchestrate",
                {"text": "test", "token": r.json["access_token"]},
            )

            AssertThat(mock_categorize_function.call_count).IsEqualTo(3)

    @patch("app.cart_query_response")
    def test_cart_query_endpoint_returns_answer(self, cart_query_mock) -> None:
        def test_fn():
            yield {"choices": [{"delta": {"content": "$5"}}]}

        cart_query_mock.return_value = test_fn()

        self.test_socket.emit(
            "cart-query",
            {
                "text": "How much milk",
                "token": create_access_token(identity="test"),
            },
        )

        AssertThat(cart_query_mock).WasCalled().Once().With(
            "test", "How much milk"
        )

        received = self.test_socket.get_received()
        AssertThat(received[0]["name"]).IsEqualTo("cart-query")
        AssertThat(received[0]["args"][0]["text"]).IsEqualTo("$5")

    @patch("app.json_recipe_from_product_catalog")
    def test_auto_add_to_cart_socket_loads_cart(
        self, json_recipe_mock
    ) -> None:
        r = self.client.get("/refresh-session")

        def test_fn():
            yield {
                "choices": [
                    {"delta": {"content": '{"id": 1, "name": "Milk"}'}}
                ]
            }

        json_recipe_mock.return_value = test_fn()

        self.test_socket.emit(
            "auto-add-to-cart",
            {"text": "breakfast pls", "token": r.json["access_token"]},
        )
        received = self.test_socket.get_received()

        AssertThat(json_recipe_mock).WasCalled().Once().With("breakfast pls")
        AssertThat(received[0]["name"]).IsEqualTo("auto-add-to-cart")
        AssertThat(received[0]["args"][0]["cart"]).IsEqualTo(
            [{"id": 1, "name": "Milk", "quantity": 1}]
        )
        cart = Session.query.first().cart

        AssertThat(cart).IsEqualTo([{"id": 1, "name": "Milk", "quantity": 1}])
