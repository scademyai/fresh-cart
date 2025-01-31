# ************************************************************************* #
#                                                                           #
#                           EXERCISES START BELOW                           #
#                                                                           #
# ************************************************************************* #


# EXERCISE 1. - FreshBot
# Your task is to provide a usable context for the AI model
# - Name, website it operates on, and any other relevant information.
# - Can only answer questions about the website.
# - Website address, website endpoints
# - Privacy policy, terms of conditions

# Extend this context
ex1_freshbot_context = f"""

"""

# EXERCISE 2. - Simple recipe
# Your task is to provide a usable context for the AI model
# - It should ensure that it answers to any recipe request, but nothing else.

# Extend this context
ex2_text_recipe_context = f"""

"""


# EXERCISE 3. - Orchestration
# Your task is to provide a usable context for the AI model
# - It should decide what topic the user asks about

# Extend this context
ex3_categorization_context = f"""

"""


# EXERCISE 4. - Formatted response
# Your task is to provide a usable context for the AI model
# - It should ensure that the returned ingredients are JSON formatted

# Extend this context
ex4_json_recipe_context = f"""

"""


def ex5_json_recipe_from_product_catalog_context() -> str:
    # EXERCISE 5. - Product catalog recipe
    # Your task is to provide a usable context for the AI model
    # - It should return ingredients only from the product catalog
    # - Ingredients should be JSON formatted
    # - They should contain id, name, quantity, and price
    # - Products can be queried from:
    # - from .db import get_every_product

    from .db import get_every_product

    products = get_every_product()
    products_context = "Products in the catalog:\n"

    for product in products:
        products_context += f"{product.json()}\n---\n"

    # Extend this context
    context = f"""

    """

    return context
