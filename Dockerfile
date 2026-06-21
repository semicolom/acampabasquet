FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

WORKDIR /app/src

ENV DJANGO_SETTINGS_MODULE=settings.dev

EXPOSE 8000
