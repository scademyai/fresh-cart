import os

import openai
import tiktoken
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from lib.ai.models import openai_api_response
from lib.models.documents import Document
from lib.models.products import Product

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_product_catalog():
    products = __get_products()

    for product in products:
        embed(product.name)


def embed(string: str) -> None:
    embedding = __create_embedding(string)
    session = __get_db_session()

    db_document = Document(content=string, embedding=embedding)
    session.add(db_document)
    session.commit()
    session.close()


def query_embedding(search: str):
    embedding = __create_embedding(search)
    documents = __find_related_documents(embedding)

    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_count = 0
    context_text = ""

    for document in documents:
        content = document.content
        encoded = tokenizer.encode(content)
        token_count += len(encoded)

        if token_count > 1500:
            break

        context_text += f"{content.strip()}\n---\n"

    prompt = f"""
        You are are an AI assistant for a website called Fresh Cart that specializes
        in selling ingredients to recipes based on the recipe given by the user.
        Here is our product catalog line by line:

        {context_text}

        Answer the following question/request based on the above product catalog:
        {search}
    """

    response = openai_api_response(prompt)
    print(response["choices"][0]["message"]["content"])


def __get_products() -> list[Product]:
    session = __get_db_session()

    documents = session.query(Product).all()
    session.close()

    return documents


def __create_embedding(string: str) -> None:
    input_str = string.replace("\n", " ")
    embedding_response = openai.Embedding.create(
        model="text-embedding-ada-002", input=input_str
    )
    embedding = embedding_response["data"][0]["embedding"]

    return embedding


def __get_db_session():
    engine = create_engine(os.environ["DATABASE_URL"])
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def __find_related_documents(search: str) -> list[Document]:
    sql = text(
        """
        SELECT *
        FROM match_documents(
            CAST(:embedding AS vector),
            CAST(:similarity_threshold AS float),
            CAST(:match_count AS int)
        )
    """
    )

    parameters = {
        "embedding": search,
        "similarity_threshold": 0.78,
        "match_count": 10,
    }

    documents = []

    session = __get_db_session()
    documents = session.execute(sql, parameters).fetchall()
    session.close()

    return documents


if __name__ == "__main__":
    embed_product_catalog()
