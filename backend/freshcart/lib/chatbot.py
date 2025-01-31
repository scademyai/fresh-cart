import os

from langsmith import traceable

from .ai.llm_adapter import categorize_message, completion
from .contexts import (
    ex1_freshbot_context,
    ex2_text_recipe_context,
    ex3_categorization_context,
    ex4_json_recipe_context,
    ex5_json_recipe_from_product_catalog_context,
    ex7_sql_injection_context,
)
from .logger import log
from .stream_utils import stream, stream_json, stream_text

# ************************************************************************* #
#                                                                           #
#                           EXERCISES START BELOW                           #
#                                                                           #
# ************************************************************************* #
# fmt: off

@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
)
def freshbot_entry_point(message: dict):
    log(f"freshbot: {message['text']}")

    # EXERCISE 1.
    #ex1_freshbot_website(message["text"])

    # EXERCISE 2. Comment out the line above and uncomment the line below.
    #ex2_recipe_suggestion(message["text"])

    # EXERCISE 3. Comment out the line above and uncomment the line below.
    ex3_orchestrate(message["text"])


def ex1_freshbot_website(message: str):
    # EXERCISE 1. - FreshBot
    # Your task is to implement a basic chatbot with static context.

    stream(completion(ex1_freshbot_context, message, ex_title = "ex1_freshbot_website"))


def ex2_recipe_suggestion(message: str):
    # EXERCISE 2. - Simple recipe
    # Your task is to implement a recipe suggestor extending a context.

    stream(completion(ex2_text_recipe_context, message, ex_title = "ex2_recipe_suggestion"))

@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
)
def ex3_orchestrate(message: str):
    # EXERCISE 3. - Orchestrate
    # Your task is to implement an orchestrator that routes the user's
    # request to the correct handler prompt.

    category = categorize_message(
        ex3_categorization_context, message, trials=2
    )

    log(f"identified as: {category}")
    if category == "website":
        ex1_freshbot_website(message)
    elif category == "recipe":
        #ex2_recipe_suggestion(message)

        # EXERCISE 4. Comment out the line above and uncomment the line below.
        #ex4_json_recipe(message)

        # EXERCISE 5. Comment out the line above and uncomment the line below.
        ex5_product_catalog_recipe(message)
    elif category == "product":
        ex7_sql_injection(message)
    else:
        stream_text("I don't understand.")


def ex4_json_recipe(message: str):
    # EXERCISE 4. - JSON recipe
    # Your task is to stream parsable JSON fragments.
    # Each message should be a valid JSON object.
    # Fragment format: { "name": "Milk", "quantity": "1" }

    stream_json(completion(ex4_json_recipe_context, message, ex_title = "ex4_json_recipe"))


def ex5_product_catalog_recipe(message: str):
    # EXERCISE 5. - Product catalog recipe
    # Your task is to implement a recipe suggestor only containing
    # items from the product catalog.

    stream_json(
        completion(
            ex5_json_recipe_from_product_catalog_context(), message, ex_title = "ex5_product_catalog_recipe"
        )
    )
# fmt: on


def ex7_sql_injection(message: str):
    # EXERCISE 7. - SQL Injection - Product information
    # Your task is to make the model run a malicious query
    response = completion(
        ex7_sql_injection_context,
        message,
        stream=False,
        ex_title="ex7_sql_injection",
    )
    query = response.choices[0].message.content

    try:
        from .db import execute_query

        products = execute_query(query)

        i = 0
        for product in products:
            for col in product:
                if i > 0:
                    stream_text(", ")
                stream_text(col)
                i += 1

        if i == 0:
            stream_text("Something went wrong.")
    except:
        stream_text("Something went wrong.")
