import os
import time

from langsmith import traceable
from openai import OpenAI

client = OpenAI()

MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"


@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
    run_type="llm",
)
def completion(prompt: str, stream: bool = True, ex_title: str = ""):
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt},
        ],
        store=True,
        metadata={"type": "freshcart", "title": ex_title},
        stream=stream,
    )


def embed_text(text: str) -> [float]:
    ret = client.embeddings.create(model=EMBEDDING_MODEL, input=text)

    return ret.data[0].embedding


@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
)
def completion_text(prompt: str):
    return (
        completion(prompt, False, "text completion").choices[0].message.content
    )


@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
)
def categorize_message(prompt: str, trials: int = 1) -> str:
    category = ""

    for _ in range(trials):
        category = completion_text(prompt)

        if category in ("website", "recipe", "product"):
            return category

        time.sleep(0.2)

    return "unknown"
