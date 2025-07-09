# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy app code
COPY manufac_assignment ./manufac_assignment
COPY data ./data

# Expose port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "manufac_assignment.main:app", "--host", "0.0.0.0", "--port", "8000"] 