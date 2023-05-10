from unittest.mock import patch
from uuid import uuid4

from truth.truth import AssertThat

from lib.contexts import (
    cart_context,
    cart_query_context,
    categorization_context,
    freshbot_context,
    json_recipe_context,
    json_recipe_from_product_catalog_context,
    product_catalog_context,
    text_recipe_context,
)
from lib.models import db
from lib.models.products import Product
from lib.models.sessions import Session
from tests import AppTestCase, DbMixin


class TestContexts(DbMixin, AppTestCase):
    def test_text_recipe_context_contains_example(self) -> None:
        response = text_recipe_context("Test product")

        AssertThat(response).Contains("1/2 ripe avocado")

    def test_text_recipe_context_contains_users_input(self) -> None:
        response = text_recipe_context("Test recipe for me")

        AssertThat(response).Contains("Test recipe for me")

    def test_freshbot_context_contains_website_info(self) -> None:
        response = freshbot_context("test-question")

        AssertThat(response).Contains(
            "Based on the above context, answer the user's question."
        )

    def test_freshbot_context_contains_users_input(self) -> None:
        response = freshbot_context("test-question")

        AssertThat(response).Contains("test-question")

    def test_json_recipe_context_contains_recipe_prompt(self) -> None:
        response = json_recipe_context("test-question")

        AssertThat(response).Contains('{"name": "Milk", "quantity": "1"}')
        AssertThat(response).Contains(
            "Give a recipe for the user based on the above context."
        )

    def test_json_recipe_context_contains_users_input(self) -> None:
        response = json_recipe_context("test-question")

        AssertThat(response).Contains("test-question")

    def test_categorization_response_contains_website_topic_example(
        self,
    ) -> None:
        response = categorization_context("Terms & Conditions")

        AssertThat(response).Contains("Your answer: website")

    def test_categorization_response_contains_cart_example(self) -> None:
        response = categorization_context("Cart total cost")

        AssertThat(response).Contains("Your answer: cart")

    def test_categorization_response_contains_general_topic_example(
        self,
    ) -> None:
        response = categorization_context("A recipe for a breakfast")

        AssertThat(response).Contains("Your answer: general")

    def test_categorization_response_contains_users_input(self) -> None:
        response = categorization_context("A recipe for a breakfast")

        AssertThat(response).Contains("A recipe for a breakfast")

    def test_product_catalog_context_contains_every_product(self) -> None:
        p_1 = Product(name="Test product 1", price=10.0)
        p_2 = Product(name="Test product 2", price=20.0)
        db.session.add(p_1)
        db.session.add(p_2)
        db.session.commit()

        response = product_catalog_context()

        AssertThat(response).Contains("Products in the catalog:\n")
        AssertThat(response).Contains(f"{p_1.json()}\n---\n")
        AssertThat(response).Contains(f"{p_2.json()}\n---\n")

    @patch("lib.contexts.product_catalog_context")
    def test_json_recipe_from_product_catalog_context_returns_json_ingredients_list(
        self, mock_context
    ) -> None:
        mock_context.return_value = f"{{test-catalog}}"

        response = json_recipe_from_product_catalog_context(
            "test-recipe-request"
        )

        AssertThat(response).Contains("{test-catalog}")
        AssertThat(response).Contains(
            '{"id": 1, "name": "Milk", "quantity": "1", "price": "0.50"}'
        )

    def test_cart_context_contains_cart(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 1, "price": 1.0}]
        session = Session(id=session_id, cart=cart)

        db.session.add(session)
        db.session.commit()

        response = cart_context(session_id)

        AssertThat(response).Contains("Cart:")
        AssertThat(response).Contains(str(cart))

    def test_cart_query_context_contains_explanation_prompt(self) -> None:
        session = Session(id=uuid4())
        db.session.add(session)
        db.session.commit()

        response = cart_query_context(session.id, "test-question")

        AssertThat(response).Contains(
            "Answer the user's question based on the above cart"
        )

    def test_cart_query_context_contains_user_input(self) -> None:
        session = Session(id=uuid4())
        db.session.add(session)
        db.session.commit()

        response = cart_query_context(session.id, "test-question")

        AssertThat(response).Contains("test-question")
