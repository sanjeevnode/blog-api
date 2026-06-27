FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

# Install dependencies using pip (standard fail-safe)
RUN pip install --no-cache-dir \
        fastapi "uvicorn[standard]" "sqlalchemy[asyncio]" asyncpg alembic \
        pydantic pydantic-settings "python-jose[cryptography]" redis boto3 \
        loguru pytz sqlalchemy-utils python-multipart aiosmtplib \
        email-validator httpx

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
