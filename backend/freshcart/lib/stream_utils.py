import json

from flask import current_app, request

from .logger import log

MESSAGE_TYPE = "freshbot"


def stream(generator):
    for token in generator:
        if content := token.choices[0].delta.content:
            current_app.extensions["socketio"].emit(
                MESSAGE_TYPE, {"text": content}, room=request.sid
            )


def stream_text(message: str):
    current_app.extensions["socketio"].emit(
        MESSAGE_TYPE,
        {"text": message},
        room=request.sid,
    )


# ************************************************************************* #
#                                                                           #
#                           EXERCISES START BELOW                           #
#                                                                           #
# ************************************************************************* #


def stream_json(generator):
    # EXERCISE 4.
    # Your task is to stream parsable JSON fragments.
    # Each message should be a valid JSON object.
    # Fragment format: { "name": "Milk", "quantity": "1" }

    log("buffering chunks...")
    chunks = ""
    for token in generator:
        if content := token.choices[0].delta.content:
            chunks += content
            log(f"chunks: {chunks}")
        try:
            j = json.loads(chunks)
            current_app.extensions["socketio"].emit(
                MESSAGE_TYPE, {"json": j}, room=request.sid
            )
            log(f"emit: {j}")
            chunks = ""
            continue
        except json.JSONDecodeError:
            log("failed to parse")
            continue
