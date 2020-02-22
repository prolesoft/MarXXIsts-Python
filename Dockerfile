FROM python:3.7-alpine
WORKDIR /marxxists
RUN apk add --no-cache \
    build-base \
    gcc \
    libpq \
    linux-headers \
    musl-dev \
    postgresql-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
