# ************************************************************************* #
#                                                                           #
#                           EXERCISES START BELOW                           #
#                                                                           #
# ************************************************************************* #


def ex1_freshbot_context(prompt: str) -> str:
    # EXERCISE 1. - FreshBot
    # Your task is to provide a usable context for the AI model
    # - Name, website it operates on, and any other relevant information.
    # - Can only answer questions about the website.
    # - Website address, website endpoints
    # - Privacy policy, terms of conditions

    # Extend this context
    context = f"""
        Context:
            - Your name: FreshBot
            - Website you operate on: Fresh Cart
            - Link to Privacy Policy: http://localhost:4200/privacy-policy
            - Link to Terms of Service: http://localhost:4200/terms-of-service
            - Operator of Fresh Cart: SCADEMY Human-AI Symbiosis Academy, a company teaching other organizations how they can integrate AI into their processes.
            - Website description: Fresh Cart is an e-commerce website selling ingredients to any kind of recipe you can think of.
              With Fresh Cart's revolutionary AI assistant, you are able to describe your needs and receive recommendations of ingredients based on your preferences.
              The AI will collect every available product from the product catalog and put it in your basket.
            - Website address: http://localhost:4200
            - Website endpoints:
                - /: Home, where you see our motto. The chatbot on the side is visible on every page.
                - /shop: Here you can browse the product catalog and add products to your cart.
                - /cart: Shopping cart with your selected products.
        ---
        Based on the above context, answer the user's question.
        Only use the above context, do not use any other information.
        
        User question: {prompt}
        Your answer:
    """

    return context


def ex2_text_recipe_context(prompt: str) -> str:
    # EXERCISE 2. - Simple recipe
    # Your task is to provide a usable context for the AI model
    # - It should ensure that it answers to any recipe request, but nothing else.

    # Extend this context
    context = f"""
        {prompt}
    """
    return context


def ex3_categorization_context(prompt: str) -> str:
    # EXERCISE 3. - Orchestration
    # Your task is to provide a usable context for the AI model
    # - It should decide what topic the user asks about

    # Extend this context
    context = f"""
        {prompt}
    """

    return context


def ex4_json_recipe_context(prompt: str) -> str:
    # EXERCISE 4. - Formatted response
    # Your task is to provide a usable context for the AI model
    # - It should ensure that the returned ingredients are JSON formatted

    # Extend this context
    context = f"""
        {prompt}
    """
    return context


def ex5_json_recipe_from_product_catalog_context(prompt: str) -> str:
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
        {prompt}
    """

    return context
