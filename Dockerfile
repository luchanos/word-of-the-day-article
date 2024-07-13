FROM python:3.11.5-alpine

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo

RUN pip3 install -U pip==24.0 && pip3 install poetry==1.8.3

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && poetry install --no-root

EXPOSE 8080
