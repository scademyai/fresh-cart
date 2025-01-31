import os
import time

from langsmith import traceable
from openai import OpenAI

client = OpenAI()

MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"


@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
    run_type="llm",
)
def completion(
    system_prompt: str, prompt: str, stream: bool = True, ex_title: str = ""
):
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        store=True,
        metadata={"type": "freshcart", "title": ex_title},
        stream=stream,
    )


def embed_text(text: str) -> list[float]:
    ret = client.embeddings.create(model=EMBEDDING_MODEL, input=text)

    return ret.data[0].embedding


@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
)
def completion_text(system_prompt: str, prompt: str):
    return (
        completion(system_prompt, prompt, False, "text completion")
        .choices[0]
        .message.content
    )


@traceable(
    tags=[os.environ.get("LANGCHAIN_TAG")],
)
def categorize_message(
    system_prompt: str, prompt: str, trials: int = 1
) -> str:
    category = ""

    for _ in range(trials):
        category = completion_text(system_prompt, prompt)

        if category in ("website", "recipe"):
            return category

        time.sleep(0.2)

    return "unknown"
