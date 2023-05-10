import unittest
from unittest.mock import patch
from uuid import uuid4

from truth.truth import AssertThat

from lib.ai import models


class TestModels(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_freshbot_stream_streams_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("This is a")
            yield test_content("test message")

        openai_create_mock.return_value = test_generator()
        models.freshbot_stream("text")

        AssertThat(openai_create_mock.call_args.kwargs.get("stream")).IsTrue()

    @patch("openai.ChatCompletion.create")
    def test_freshbot_stream_returns_generator_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("This is a")
            yield test_content("test message")

        openai_create_mock.return_value = test_generator()
        response = models.freshbot_stream("text")
        response_as_list = list(response)

        AssertThat(
            response_as_list[0]["choices"][0]["delta"]["content"]
        ).IsEqualTo("This is a")
        AssertThat(
            response_as_list[1]["choices"][0]["delta"]["content"]
        ).IsEqualTo("test message")

    @patch("time.sleep")
    @patch("openai.ChatCompletion.create")
    def test_fresbot_stream_handles_errors(
        self, openai_create_mock, time_mock
    ):
        time_mock.return_value = None
        openai_create_mock.side_effect = Exception("BOOM")

        response = models.freshbot_stream("text")
        response_as_list = list(response)

        message = [
            "Our ",
            "language ",
            "model ",
            "is ",
            "currently ",
            "unavailable. ",
            "Try ",
            "again ",
            "later.",
        ]

        for index, word in enumerate(message):
            AssertThat(
                response_as_list[index]["choices"][0]["delta"]["content"]
            ).IsEqualTo(word)

    @patch("openai.ChatCompletion.create")
    def test_text_recipe_response_streams_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("Here is a")
            yield test_content("recipe for 5 people")

        openai_create_mock.return_value = test_generator()
        models.text_recipe_response("text")

        AssertThat(openai_create_mock.call_args.kwargs.get("stream")).IsTrue()

    @patch("openai.ChatCompletion.create")
    def test_text_recipe_response_returns_generator_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("Here is a")
            yield test_content("recipe for 5 people")

        openai_create_mock.return_value = test_generator()
        response = models.text_recipe_response("text")
        response_as_list = list(response)

        AssertThat(
            response_as_list[0]["choices"][0]["delta"]["content"]
        ).IsEqualTo("Here is a")
        AssertThat(
            response_as_list[1]["choices"][0]["delta"]["content"]
        ).IsEqualTo("recipe for 5 people")

    @patch("openai.ChatCompletion.create")
    def test_json_recipe_response_streams_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("Here is a")
            yield test_content("recipe for 5 people")

        openai_create_mock.return_value = test_generator()
        models.json_recipe_response("text")

        AssertThat(openai_create_mock.call_args.kwargs.get("stream")).IsTrue()

    @patch("openai.ChatCompletion.create")
    def test_json_recipe_response_returns_generator_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("Here is a")
            yield test_content("recipe for 5 people")

        openai_create_mock.return_value = test_generator()
        response = models.json_recipe_response("text")
        response_as_list = list(response)

        AssertThat(
            response_as_list[0]["choices"][0]["delta"]["content"]
        ).IsEqualTo("Here is a")
        AssertThat(
            response_as_list[1]["choices"][0]["delta"]["content"]
        ).IsEqualTo("recipe for 5 people")

    @patch("lib.contexts.product_catalog_context")
    @patch("openai.ChatCompletion.create")
    def test_json_recipe_from_product_catalog_returns_response(
        self, openai_create_mock, product_catalog_mock
    ) -> None:
        def test_content(text: str) -> dict:
            yield {"choices": [{"delta": {"content": text}}]}

        openai_create_mock.return_value = test_content(
            '{"a json": "response"}'
        )
        product_catalog_mock.return_value = '{"a": "b"}'
        response = models.json_recipe_from_product_catalog("A dinner please")
        response_as_list = list(response)

        AssertThat(
            response_as_list[0]["choices"][0]["delta"]["content"]
        ).IsEqualTo('{"a json": "response"}')

    @patch("openai.ChatCompletion.create")
    def test_categorize_question_returns_singe_word_response(
        self, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"message": {"content": text}}]}

        openai_create_mock.return_value = test_content("general")
        response = models.categorize_question("A recipe of a cake")

        AssertThat(response).IsEqualTo("general")

    @patch("openai.ChatCompletion.create")
    @patch("lib.ai.models.cart_query_context")
    def test_cart_query_response_streams_response(
        self, cart_query_context_mock, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("Dairy products cost")
            yield test_content("$5 in your cart together")

        openai_create_mock.return_value = test_generator()
        cart_query_context_mock.return_value = "text"

        models.cart_query_response(uuid4(), "text")
        AssertThat(openai_create_mock.call_args.kwargs.get("stream")).IsTrue()

    @patch("openai.ChatCompletion.create")
    @patch("lib.ai.models.cart_query_context")
    def test_cart_query_response_returns_generator_response(
        self, cart_query_context_mock, openai_create_mock
    ) -> None:
        def test_content(text: str) -> dict:
            return {"choices": [{"delta": {"content": text}}]}

        def test_generator():
            yield test_content("Dairy products cost")
            yield test_content("$5 in your cart together")

        openai_create_mock.return_value = test_generator()
        cart_query_context_mock.return_value = "text"

        response = models.cart_query_response(uuid4(), "text")
        response_as_list = list(response)

        AssertThat(
            response_as_list[0]["choices"][0]["delta"]["content"]
        ).IsEqualTo("Dairy products cost")
        AssertThat(
            response_as_list[1]["choices"][0]["delta"]["content"]
        ).IsEqualTo("$5 in your cart together")
