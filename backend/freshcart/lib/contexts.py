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
        Context:
            - Even if the user doesn't ask something specific, give them a recipe that is close to their request.
            - Don't answer anything else. Not even the name of the recipe.

            Example request:
                Breakfast for 1 person
            Example return:
                Here is a delicious and healthy breakfast recipe that you can make for one person:
                Avocado Toast with Egg:

                Ingredients:
                - 1 slice of whole grain bread
                - 1/2 ripe avocado
                - 1 egg
                - Salt and pepper to taste
                - Optional toppings: sliced tomato, feta cheese, everything bagel seasoning

                Instructions:
                1. Toast the slice of bread.
                2. While the bread is toasting, mash the avocado in a small bowl and add salt and pepper to taste.
                3. Fry the egg in a non-stick skillet until the white is set and the yolk is still runny.
                4. When the toast is done, spread the mashed avocado on top.
                5. Place the fried egg on top of the avocado toast.
                6. Finish by adding any optional toppings you desire.

                Enjoy your delicious and healthy breakfast!
        ---
        Give a recipe for the user based on the above context.
        
        User request: {prompt}
        Your answer:
    """
    return context


def ex3_categorization_context(prompt: str) -> str:
    # EXERCISE 3. - Orchestration
    # Your task is to provide a usable context for the AI model
    # - It should decide what topic the user asks about

    # Extend this context
    context = f"""
        Decide whether the user asked something about the website, about their cart, or about a general topic like a recipe for a breakfast.
        
        If the question is about the website, return 'website'.
        If the question is about a recipe, return 'recipe'.
        
        Example question: Show me the terms and conditions.
        Your answer: website
        
        Example question: Write me a recipe for a dinner of 5 people.
        Your answer: recipe

        User input: {prompt}
        Your answer:
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
