IMAGE_VERSION=$(shell git describe --exact 2>/dev/null || git rev-parse --short=10 HEAD 2>/dev/null)

build:
	docker build -t marxxists:$(IMAGE_VERSION) .

run:
	docker-compose up --build -d

stop:
	docker-compose down
