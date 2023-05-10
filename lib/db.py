import json
import os

from sqlalchemy import create_engine

from lib.ai.models import openai_api_response
from lib.models.products import Product

engine = create_engine(os.environ.get("DATABASE_URL"))


def read(module_path: str) -> str:
    file_path = module_path.replace(".", os.path.sep) + ".py"

    try:
        with open(file_path, "r") as file:
            contents = file.read()
    except FileNotFoundError:
        print(f"File {file_path} not found")
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

    api_response = openai_api_response(
        model_string + table_context + query_context + clearing_context
    )
    sql = json.loads(str(api_response))["choices"][0]["message"].get("content")
    return sql


def execute_query(query):
    return engine.execute(query)


def get_every_product() -> list[Product]:
    products = Product.query.all()
    return products
