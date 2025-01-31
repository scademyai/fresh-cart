import os

from sqlalchemy import create_engine, text

from .logger import log
from .models.products import Product

engine = create_engine(os.environ.get("DATABASE_URL"))


def read(module_path: str) -> str:
    file_path = module_path.replace(".", os.path.sep) + ".py"

    try:
        with open(file_path, "r") as file:
            contents = file.read()
    except FileNotFoundError:
        contents = ""

    return contents


def execute_query(query):
    log("running query: " + query)

    with engine.connect() as connection:
        result = connection.execute(text(query))
        connection.commit()
        return result


def get_every_product() -> list[Product]:
    return Product.query.all()
