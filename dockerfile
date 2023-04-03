# Use the official Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="$HOME/.local/bin:$PATH"

# Copy the .whl package file
COPY dist/ /tmp/dist

# Install the .whl package
RUN pip install /tmp/dist/tag_a_bird_backend-0.1.0-py3-none-any.whl

# Install Gunicorn
RUN pip install gunicorn

# Expose the port the app runs on
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "tag_a_bird_backend.app:create_app()"]
