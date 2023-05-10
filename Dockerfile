FROM python:3.11.3-alpine3.17

RUN apk update && apk upgrade
RUN apk add --no-cache curl chromium postgresql-libs nodejs=18.14.2-r0 yarn=1.22.19-r0 && \
    apk add --no-cache --virtual .build-deps gcc g++ rustup musl-dev postgresql-dev libffi-dev && \
    rustup-init -y

RUN yarn global add @angular/cli

ENV CHROME_BIN=/usr/bin/chromium-browser

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/.poetry python - --version 1.4.2 && \
    ln -s /root/.poetry/bin/poetry /usr/local/bin/poetry

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN source /root/.cargo/env && poetry install && yarn install --cwd client && apk del .build-deps
