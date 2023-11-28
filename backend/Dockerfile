FROM python:3.11.5-alpine3.17

RUN apk update && apk upgrade
RUN apk add --no-cache curl postgresql-dev g++

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/.poetry python - --version 1.4.2 && \
    ln -s /root/.poetry/bin/poetry /usr/local/bin/poetry

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN poetry install
