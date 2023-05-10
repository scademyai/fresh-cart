import json
import os
from uuid import uuid4

import jwt
from flask import (
    Flask,
    after_this_request,
    jsonify,
    request,
    send_from_directory,
)
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_socketio import SocketIO

from lib.ai.models import (
    cart_query_response,
    freshbot_stream,
    json_recipe_from_product_catalog,
    text_recipe_response,
)
from lib.db import execute_query, get_every_product, query_formatter
from lib.session import (
    add_product_to_cart,
    create_session,
    delete_cart,
    delete_from_cart,
    get_cart,
)


def __configure_cors(app):
    CORS(app, origins=["http://localhost:4200"])


def __init_db(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["DATABASE_URL"] = os.environ["DATABASE_URL"]

    from lib.models import init_db

    init_db(app)


@jwt_required()
def renew_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    @after_this_request
    def set_access_token(response):
        response.headers["Access-Token"] = access_token
        return response

    return access_token


def create_app():
    app = Flask(__name__, static_folder="./client/dist")
    socketio = SocketIO(app, cors_allowed_origins="*")
    app.secret_key = "very-secret-key"

    __configure_cors(app)
    __init_db(app)
    JWTManager(app)

    @app.route("/refresh-session", methods=["GET"])
    def refresh_session():
        session_id = uuid4()
        access_token = create_access_token(identity=session_id)
        create_session(session_id)

        @after_this_request
        def set_access_token(response):
            response.headers["Access-Token"] = access_token
            return response

        return jsonify(access_token=access_token)

    @app.route("/products", methods=["GET"])
    @jwt_required()
    def products():
        renew_token()
        products = get_every_product()
        products_json = [p.json() for p in products]
        return products_json

    @app.route("/cart/<int:product_id>", methods=["DELETE"])
    @jwt_required()
    def remove_item(product_id):
        renew_token()
        session_id = get_jwt_identity()
        cart = delete_from_cart(session_id, product_id)

        return {"cart": cart}, 200

    @app.route("/cart", methods=["GET", "POST", "DELETE"])
    @jwt_required()
    def cart():
        renew_token()
        session_id = get_jwt_identity()
        if request.method == "GET":
            cart = get_cart(session_id)
        elif request.method == "DELETE":
            cart = delete_cart(session_id)
        else:
            cart = add_product_to_cart(session_id, request.json["product"])
        return {"cart": cart}, 200

    @app.route("/<path:path>")
    def serve_static(path):
        if path != "" and "." in path:
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    def stream(generator, message_type):
        for token in generator:
            if content := token["choices"][0]["delta"].get("content"):
                socketio.emit(
                    message_type, {"text": content}, room=request.sid
                )

    # ************************** EXERCISES START BELOW **************************

    # EXERCISE 1
    @socketio.on("freshbot")
    def freshbot(message: dict):
        """
        Exercise 1 - FreshBot
        Your task is to implement a model function in models.py (__freshbot_response(...)) and a model context in context.py (freshbot_context(...)).
        - Use the message as input for this function.
        - Stream the returned answer
        """

        tmp = freshbot_stream(message["text"])
        stream(tmp, "freshbot")

    # EXERCISE 2
    @socketio.on("simple-recipe")
    def simple_recipe(message: dict):
        """
        Exercise 2 - Simple recipe
        Your task is to implement a model function in models.py (text_recipe_response(...)) and a model context in context.py (text_recipe_context(...)).
        """

        model_response = text_recipe_response(message["text"])
        stream(model_response, "simple-recipe")

    # EXERCISE 3
    @socketio.on("orchestrate")
    def orchestrate(message: dict):
        """
        Exercise 3 - Orchestrate
        Your task is to implement an orchestrator that decides which model to use based on the user's input. Extend the categorize_question(...) function in models.py and its context (categorization_context(...)) in contexts.py
        """

        text = message["text"]
        session_id = jwt.decode(
            message["token"], app.secret_key, algorithms=["HS256"]
        )["sub"]

        website_answer = freshbot_stream(text)
        stream(website_answer, "orchestrate")

    # EXERCISE 4
    @socketio.on("json-recipe")
    def recipe(message: dict):
        """
        Exercise 4 - Formatted response
        Your task is to implement a model function in models.py (json_recipe_response(...)) and a model context in context.py (json_recipe_context(...)).
        - Stream the returned answer in JSON format.
        - Change the code in the previous exercise to use this new model.
        """

        tmp = text_recipe_response(message["text"])
        stream(tmp, "json-recipe")

    # EXERCISE 5
    @socketio.on("json-product-catalog-recipe")
    def json_product_catalog_recipe(message: dict):
        """
        Exercise 5 - Product catalog recipe
        Your task is to implement a model function in models.py (json_recipe_from_product_catalog(...)) and a model context in context.py (json_recipe_from_product_catalog_context(...)).
        - This model should produce recipes that can be assembled from the product catalog.
        - Stream the returned answer in JSON format.
        - Change the code in the previous exercise to use this new model.
        """

        tmp = json_recipe_from_product_catalog(message["text"])
        socketio.emit("json-product-catalog-recipe", tmp, room=request.sid)

    # EXERCISE 6
    @socketio.on("cart-query")
    def cart_query(message: dict):
        """
        Exercise 6 - Cart query
        Your task is to extend the orchestrator in Exercise 3 with an additional model that answers questions about the user's cart
        - Implement a model function in models.py (cart_query_response(...)) and a model context in context.py (cart_query_context(...)).
        - Stream the returned answer in JSON format.
        - The below code is just an example to get the user's cart. This code should be put in Exercise 3.
        """

        session_id = jwt.decode(
            message["token"], app.secret_key, algorithms=["HS256"]
        )["sub"]
        response = cart_query_response(session_id, message["text"])
        stream(response, "cart-query")

    # BONUS EXERCISE
    @socketio.on("auto-add-to-cart")
    def auto_add_to_cart(message: dict):
        """
        Bonus Exercise - Auto add to cart
        Your task is to combine already written functions to implement a feature that adds ingredients to the user's cart automatically.
        """

        session_id = jwt.decode(
            message["token"], app.secret_key, algorithms=["HS256"]
        )["sub"]
        response = cart_query_response(session_id, message["text"])
        stream(response, "cart-query")

    # ADVANCED COURSE
    @socketio.on("search")
    def search(message: dict):
        response = query_formatter("products", message["text"])
        items = execute_query(response)
        items_list = list(items)
        for item in items_list:
            socketio.emit("search", f"- {item[1]}\n", room=request.sid)

    return app, socketio


app, socketio = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
