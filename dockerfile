# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the content of the root and subfolders to the working directory
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Set environment variables from the build arguments
ARG FLASK_APP
ARG FLASK_DATABASE_URI
ARG FLASK_SQLALCHEMY_TRACK_MODIFICATIONS
ARG FLASK_DEBUG
ARG FLASK_TESTING
ARG FLASK_SECRET_KEY
ARG COREO_API_KEY
ARG ADMIN_CREDENTIALS_EMAIL
ARG ADMIN_CREDENTIALS_PW

ENV FLASK_APP=$FLASK_APP
ENV FLASK_DATABASE_URI=$FLASK_DATABASE_URI
ENV FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=$FLASK_SQLALCHEMY_TRACK_MODIFICATIONS
ENV FLASK_DEBUG=$FLASK_DEBUG
ENV FLASK_TESTING=$FLASK_TESTING
ENV FLASK_SECRET_KEY=$FLASK_SECRET_KEY
ENV COREO_API_KEY=$COREO_API_KEY
ENV ADMIN_CREDENTIALS_EMAIL=$ADMIN_CREDENTIALS_EMAIL
ENV ADMIN_CREDENTIALS_PW=$ADMIN_CREDENTIALS_PW

# Expose the port the app runs on
EXPOSE 8000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tag_a_bird_backend.app:app"]