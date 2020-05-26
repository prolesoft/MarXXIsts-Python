.PHONY: build

IMAGE_VERSION=$(shell git describe --exact 2>/dev/null || git rev-parse --short=10 HEAD 2>/dev/null)

run:
	docker-compose up --build -d

stop:
	docker-compose down

build:
	docker build -t marxxists:$(IMAGE_VERSION) .
