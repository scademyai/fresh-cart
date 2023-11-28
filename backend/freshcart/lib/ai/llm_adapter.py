import time

from openai import OpenAI

client = OpenAI()

MODEL = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-ada-002"


def completion(prompt: str, stream: bool = True):
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=stream,
    )


def embed_text(text: str) -> [float]:
    ret = client.embeddings.create(model=EMBEDDING_MODEL, input=text)

    return ret.data[0].embedding


def completion_text(prompt: str):
    return completion(prompt, False).choices[0].message.content


def categorize_message(prompt: str, trials: int = 1) -> str:
    category = ""

    for _ in range(trials):
        category = completion_text(prompt)

        if category in ("website", "recipe"):
            return category

        time.sleep(0.2)

    return "unknown"
