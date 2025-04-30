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

all: clean dev ## Clean Install and Build

install:
	pip install .

dev:
	pip install ".[test,lint,typing]"

build:
	pip install build
	python -m build .

clean: ## clean
	git clean -fdx

build-docker: ## Build multi-architecture Docker images
	docker buildx create --name multiarch-builder --use --driver docker-container || true
	docker buildx inspect --bootstrap
	docker buildx build --platform linux/amd64,linux/arm64 \
        --build-arg BASE_IMAGE=python:3.10-slim \
        --build-arg BASE_IMAGE=python:3.10-slim \
        -t czqiliang/jupyter-mcp-server:${VERSION} \
        -t czqiliang/jupyter-mcp-server:latest \
		--pull=false \
		--push \
        .

build-docker-local-only:
	docker build -t czqiliang/jupyter-mcp-server:${VERSION} .
	docker image tag czqiliang/jupyter-mcp-server:${VERSION} czqiliang/jupyter-mcp-server:latest

start-docker:
	docker run -i --rm \
	  -e SERVER_URL=http://127.0.0.1:8888 \
	  -e TOKEN=YOUR_SECURE_TOKEN \
	  -e NOTEBOOK_PATH=notebook.ipynb \
	  --network=host \
	  czqiliang/jupyter-mcp-server:latest

pull-docker:
	docker image pull czqiliang/jupyter-mcp-server:latest

push-docker: ## Push multi-architecture Docker images
	@echo "Images are pushed during the build-docker step with --push."

# push-docker:
# 	docker push czqiliang/jupyter-mcp-server:${VERSION}
# 	docker push czqiliang/jupyter-mcp-server:latest

claude-linux:
	NIXPKGS_ALLOW_UNFREE=1 nix run github:k3d3/claude-desktop-linux-flake \
		--impure \
		--extra-experimental-features flakes \
		--extra-experimental-features nix-command

jupyterlab:
	pip uninstall -y pycrdt datalayer_pycrdt
	pip install datalayer_pycrdt
	jupyter lab \
		--port 8888 \
		--ip 0.0.0.0 \
		--ServerApp.root_dir ./dev/content \
		--IdentityProvider.token MY_TOKEN

publish-pypi: # publish the pypi package
	git clean -fdx && \
		python -m build
	@exec echo
	@exec echo twine upload ./dist/*-py3-none-any.whl
	@exec echo
	@exec echo https://pypi.org/project/jupyter-mcp-server/#history
