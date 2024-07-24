# Use the official Python base image
FROM python:3.10

# Set the working directory
WORKDIR /tag_a_bird_backend

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the rest of the application code
COPY tag_a_bird_backend /tag_a_bird_backend

# Install Gunicorn
RUN pip install gunicorn

# Set the FLASK_APP environment variable
ENV FLASK_APP=tag_a_bird_backend.app

# Expose the port the app runs on
EXPOSE 8000

# Start Gunicorn with Flask-Migrate upgrade
CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:8000 --workers 4 'tag_a_bird_backend.app:app'"]