import os

from sqlalchemy import create_engine, text

from .ai.llm_adapter import completion_text
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


def query_formatter(table_name: str, query: str):
    model_string = read(f"lib.models.{table_name}")
    table_context = (
        "\n\nThe above code is an sqlalchemy representation of an sql class."
    )
    query_context = (
        f"\n\nWrite me an SQL query that satisfies the following: '{query}'"
    )
    clearing_context = "\n\nDo not write any explanation and introduction, just the single code block containing the query. Escape % with %% so that it can be parsed in python interpreters."

    return completion_text(
        model_string + table_context + query_context + clearing_context
    )


def execute_query(query):
    log("running query: " + query)

    with engine.connect() as connection:
        result = connection.execute(text(query))
        connection.commit()
        return result


def get_every_product() -> list[Product]:
    return Product.query.all()
