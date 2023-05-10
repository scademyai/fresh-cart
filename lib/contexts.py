from lib.models.sessions import Session


def freshbot_context(prompt: str) -> str:
    """
    Exercise 1 - FreshBot
    Your task is to provide a usable context for the AI model
    - Name, website it operates on, and any other relevant information.
    - Can only answer questions about the website.
    - Website address, website endpoints
    - Privacy policy, terms of conditions
    """

    # Extend this context
    context = f"""
        {prompt}
    """
    return context


def text_recipe_context(prompt: str) -> str:
    """
    Exercise 2 - Recipe
    Your task is to provide a usable context for the AI model
    - It should ensure that it answers to any recipe request, but nothing else.
    """

    # Extend this context
    context = f"""
        {prompt}
    """
    return context


def json_recipe_context(prompt: str) -> str:
    """
    Exercise 4 - Formatted response
    Your task is to provide a usable context for the AI model
    - It should ensure that the returned ingredients are JSON formatted
    """

    # Extend this context
    context = f"""
        {prompt}
    """
    return context


def categorization_context(prompt: str) -> str:
    """
    Exercise 3 - Orchestration
    Your task is to provide a usable context for the AI model
    - It should decide what topic the user asks about
    """

    # Extend this context
    context = f"""
        {prompt}
    """
    return context


def product_catalog_context() -> str:
    from lib.db import get_every_product

    products = get_every_product()
    context = "Products in the catalog:\n"

    for product in products:
        context += f"{product.json()}\n---\n"

    return context


def json_recipe_from_product_catalog_context(prompt: str) -> str:
    """
    Exercise 5 - Product catalog recipe
    Your task is to provide a usable context for the AI model
    - It should return ingredients only from the product catalog
    - Ingredients should be JSON formatted
    - They should contain id, name, quantity, and price
    """

    # Extend this context
    context = f"""
        {prompt}
    """

    return context


def cart_context(session_id: str) -> str:
    cart = Session.query.get(session_id).cart

    return f"""
        Cart:
        {cart}
        ---
    """


def cart_query_context(session_id: str, prompt: str) -> str:
    """
    Exercise 6 - Cart query
    Your task is to provide a usable context for the AI model
    - It should answer the user's question about the cart
    """

    # Extend this context
    context = f"""
        {prompt}
    """

    return context
