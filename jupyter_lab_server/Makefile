# Copyright (c) 2023-2024 Datalayer, Inc.
#
# BSD 3-Clause License

SHELL=/bin/bash

.DEFAULT_GOAL := default

.PHONY: clean build

VERSION = "0.0.6"

default: all ## Default target is all.

help: ## display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)



build-docker: ## Build multi-architecture Docker images
	docker buildx create --name multiarch-builder --use --driver docker-container || true
	docker buildx inspect --bootstrap
	docker buildx build --platform linux/amd64,linux/arm64 \
        --build-arg BASE_IMAGE=python:3.10-slim \
        --build-arg BASE_IMAGE=python:3.10-slim \
        -t czqiliang/jupyter_lab_for_mcp:${VERSION} \
        -t czqiliang/jupyter_lab_for_mcp:latest \
		--pull=false \
		--push \
        .

build-docker-local-only:
	docker build -t czqiliang/jupyter_lab_for_mcp:${VERSION} .
	docker image tag czqiliang/jupyter_lab_for_mcp:${VERSION} czqiliang/jupyter_lab_for_mcp:latest



pull-docker:
	docker image pull czqiliang/jupyter_lab_for_mcp:latest

push-docker: ## Push multi-architecture Docker images
	@echo "Images are pushed during the build-docker step with --push."

# push-docker:
# 	docker push czqiliang/jupyter_lab_for_mcp:${VERSION}
# 	docker push czqiliang/jupyter_lab_for_mcp:latest


