FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment inside the container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-root --no-interaction --no-ansi --without dev

COPY alembic.ini ./
COPY migrations ./migrations

# Copy the application code
COPY api ./api
COPY src ./src
COPY support-files ./support-files
# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
