FROM node:21.2-alpine3.17

RUN apk update && apk upgrade
RUN apk add --no-cache chromium

RUN corepack enable
RUN corepack prepare yarn@stable --activate

RUN npm i @angular/cli --global

ENV CHROME_BIN=/usr/bin/chromium-browser

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN yarn install
