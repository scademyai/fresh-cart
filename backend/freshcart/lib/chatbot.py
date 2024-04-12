from .ai.llm_adapter import categorize_message, completion
from .contexts import (
    ex1_freshbot_context,
    ex2_text_recipe_context,
    ex3_categorization_context,
    ex4_json_recipe_context,
    ex5_json_recipe_from_product_catalog_context,
)
from .logger import log
from .stream_utils import stream, stream_json, stream_text

# ************************************************************************* #
#                                                                           #
#                           EXERCISES START BELOW                           #
#                                                                           #
# ************************************************************************* #
# fmt: off

def freshbot_entry_point(message: dict):
    log(f"freshbot: {message['text']}")

    # EXERCISE 1.
    #ex1_freshbot_website(message)

    # EXERCISE 2. Comment out the line above and uncomment the line below.
    #ex2_recipe_suggestion(message)

    # EXERCISE 3. Comment out the line above and uncomment the line below.
    ex3_orchestrate(message)


def ex1_freshbot_website(message: dict):
    # EXERCISE 1. - FreshBot
    # Your task is to implement a basic chatbot with static context.

    stream(completion(ex1_freshbot_context(message["text"])))


def ex2_recipe_suggestion(message: dict):
    # EXERCISE 2. - Simple recipe
    # Your task is to implement a recipe suggestor extending a context.

    stream(completion(ex2_text_recipe_context(message["text"])))


def ex3_orchestrate(message: dict):
    # EXERCISE 3. - Orchestrate
    # Your task is to implement an orchestrator that routes the user's
    # request to the correct handler prompt.

    category = categorize_message(
        ex3_categorization_context(message["text"]), trials=2
    )

    log(f"identified as: {category}")
    if category == "website":
        ex1_freshbot_website(message)
    elif category == "recipe":
        #ex2_recipe_suggestion(message)

        # EXERCISE 4. Comment out the line above and uncomment the line below.
        ex4_json_recipe(message)

        # EXERCISE 5. Comment out the line above and uncomment the line below.
        #ex5_product_catalog_recipe(message)
    else:
        stream_text("I don't understand.")


def ex4_json_recipe(message: dict):
    # EXERCISE 4. - JSON recipe
    # Your task is to stream parsable JSON fragments.
    # Each message should be a valid JSON object.
    # Fragment format: { "name": "Milk", "quantity": "1" }

    stream_json(completion(ex4_json_recipe_context(message["text"])))


def ex5_product_catalog_recipe(message: dict):
    # EXERCISE 5. - Product catalog recipe
    # Your task is to implement a recipe suggestor only containing
    # items from the product catalog.

    stream_json(
        completion(
            ex5_json_recipe_from_product_catalog_context(message["text"])
        )
    )
# fmt: on
