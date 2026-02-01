FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install django-celery-beat==2.5.0 celery==5.3.4  # Добавьте эту строку

COPY src/ .

RUN python manage.py collectstatic --noinput

EXPOSE 8000