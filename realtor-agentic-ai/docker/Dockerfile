# Use a minimal base image for Python 3.11
FROM python:3.11-slim

# Set a non-root user for security best practices
ARG APP_USER=appuser
ARG APP_GROUP=appgroup
RUN groupadd -r $APP_GROUP && useradd -r -g $APP_GROUP $APP_USER

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Leverage Docker layer caching for Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/

# Create output directory for generated documents
RUN mkdir -p /app/output

# Change ownership of the working directory to the application user
RUN chown -R $APP_USER:$APP_GROUP /app

# Run as non-root user
USER $APP_USER

# Set environment variables
ENV PYTHONPATH=/app
ENV OPENAI_API_KEY=""

# Expose port
EXPOSE 8000

# Entrypoint
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
