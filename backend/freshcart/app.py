import os
from datetime import timedelta
from uuid import uuid4

from flask import Flask, after_this_request, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_socketio import SocketIO

from .lib.chatbot import freshbot_entry_point
from .lib.db import get_every_product
from .lib.models.products import Product
from .lib.session import (
    add_product_to_cart,
    create_session,
    delete_cart,
    delete_from_cart,
    get_cart,
)


def __init_db(app):
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["DATABASE_URL"] = os.environ["DATABASE_URL"]

    from .lib.models import init_db

    init_db(app)


def __init_socket_handlers(socketio):
    socketio.on_event("freshbot", freshbot_entry_point)


def create_app():
    app = Flask(__name__, static_folder="./client/dist")
    socketio = SocketIO(app, cors_allowed_origins="*")
    app.secret_key = "very-secret-key"

    __init_db(app)
    __init_socket_handlers(socketio)
    JWTManager(app)

    @app.route("/refresh-session", methods=["GET"])
    def refresh_session():
        session_id = uuid4()
        access_token = create_access_token(
            identity=session_id, expires_delta=timedelta(hours=8)
        )
        create_session(session_id)

        @after_this_request
        def set_access_token(response):
            response.headers["Access-Token"] = access_token
            return response

        return jsonify(access_token=access_token)

    @app.route("/products", methods=["GET"])
    @jwt_required()
    def products():
        products = get_every_product()
        products_json = [p.json() for p in products]
        return products_json

    @app.route("/products/<int:product_id>", methods=["GET"])
    @jwt_required()
    def get_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return {}

        return {
            "product": product.json(),
            "similar": [p.json() for p in product.similar],
        }

    @app.route("/cart/<int:product_id>", methods=["DELETE"])
    @jwt_required()
    def remove_item(product_id):
        session_id = get_jwt_identity()
        cart = delete_from_cart(session_id, product_id)

        return {"cart": cart}, 200

    @app.route("/cart", methods=["GET", "POST", "DELETE"])
    @jwt_required()
    def cart():
        session_id = get_jwt_identity()
        if request.method == "GET":
            cart = get_cart(session_id)
        elif request.method == "DELETE":
            cart = delete_cart(session_id)
        else:
            cart = add_product_to_cart(session_id, request.json["product"])
        return {"cart": cart}, 200

    return app


app = create_app()
