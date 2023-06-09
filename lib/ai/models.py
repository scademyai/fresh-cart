import os
import time

import openai

from lib.contexts import (
    cart_query_context,
    categorization_context,
    freshbot_context,
    json_recipe_context,
    json_recipe_from_product_catalog_context,
    text_recipe_context,
)

openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_api_response(text: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    return completion


def __yield_error():
    for word in [
        "Our ",
        "language ",
        "model ",
        "is ",
        "currently ",
        "unavailable. ",
        "Try ",
        "again ",
        "later.",
    ]:
        yield {"choices": [{"delta": {"content": word}}]}
        time.sleep(0.1)


def freshbot_stream(prompt: str):
    try:
        return __freshbot_response(prompt, stream=True)
    except Exception as e:
        return __yield_error()


def __freshbot_response(prompt: str, **kwargs):
    """
    Exercise 1 - FreshBot
    Implement this function using the openai python module.
    - Fill the system content
    - Fill the user content
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot called FreshBot for an e-commerce website called Fresh Cart. Your job is to answer anything related to the website, but nothing else.",
            },
            {"role": "user", "content": freshbot_context(prompt)},
        ],
        stream=kwargs.get("stream") or False,
    )
    return completion


def text_recipe_response(prompt: str):
    """
    Exercise 2 - Recipe
    Implement this function using the openai python module.
    - Fill the system content
    - Fill the user content
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot called FreshBot for an e-commerce website called Fresh Cart. Your job is to give recipes for the users.",
            },
            {"role": "user", "content": text_recipe_context(prompt)},
        ],
        stream=True,
    )
    return completion


def json_recipe_response(prompt: str):
    """
    Exercise 4 - Formatted response
    Implement this function using the openai python module.
    - Fill the system content
    - Fill the user content
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot called FreshBot for an e-commerce website called Fresh Cart. Your job is give recipes for the users.",
            },
            {"role": "user", "content": json_recipe_context(prompt)},
        ],
        stream=True,
    )
    return completion


def json_recipe_from_product_catalog(prompt: str):
    """
    Exercise 5 - Product catalog recipe
    Implement this function using the openai python module.
    - Fill the system content
    - Fill the user content
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a chatbot called FreshBot for an e-commerce website called Fresh Cart. Your job is give recipes for the users.",
            },
            {
                "role": "user",
                "content": json_recipe_from_product_catalog_context(prompt),
            },
        ],
        stream=True,
    )
    return completion


def categorize_question(prompt: str):
    """
    Exercise 3 - Orchestration
    Implement this function using the openai python module.
    - Fill the system content
    - Fill the user content
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant for a grocery store e-commerce website whose job is to categorize the user's question. You have decide whether the user asked something about the website, about their cart's content, or about a general topic like a recipe for a breakfast.",
            },
            {"role": "user", "content": categorization_context(prompt)},
        ],
    )
    return completion["choices"][0]["message"]["content"]


def cart_query_response(session_id: str, prompt: str):
    """
    Exercise 6 - Cart query
    Implement this function using the openai python module.
    - Fill the system content
    - Fill the user content
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant for a grocery store e-commerce website whose job is to answer any request about the user's cart.",
            },
            {
                "role": "user",
                "content": cart_query_context(session_id, prompt),
            },
        ],
        stream=True,
    )
    return completion
