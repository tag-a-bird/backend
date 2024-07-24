# Use the official Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the .whl package file
COPY dist/tag_a_bird_backend-0.1.0-py3-none-any.whl /tmp/tag_a_bird_backend-0.1.0-py3-none-any.whl

# Install the .whl package
RUN pip install /tmp/tag_a_bird_backend-0.1.0-py3-none-any.whl

# Install Gunicorn
RUN pip install gunicorn

# Debug: Print installed packages
RUN pip list

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "tag_a_bird_backend.app:create_app()"]