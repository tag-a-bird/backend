ARG CURRENT_ENV=${CURRENT_ENV:-dev}

FROM python:3.10-slim-buster

ENV CURRENT_ENV=$CURRENT_ENV

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false \ 
    && poetry install
