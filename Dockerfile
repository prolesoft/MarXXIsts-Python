FROM python:3.7-alpine
WORKDIR /marxxists
RUN apk add --no-cache \
    build-base \
    ca-certificates \
    gcc \
    libpq \
    linux-headers \
    musl-dev \
    wget \
    postgresql-dev && \
    wget -O /tmp/pandoc.tar.gz \
    https://github.com/jgm/pandoc/releases/download/2.2.3.2/pandoc-2.2.3.2-linux.tar.gz && \
    tar xvzf /tmp/pandoc.tar.gz --strip-components 1 -C /usr/local/ && \
    update-ca-certificates && \
    rm /tmp/pandoc.tar.gz
COPY requirements.txt .
RUN pip install -r requirements.txt
