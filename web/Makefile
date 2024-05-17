PROJECT_NAME = airdelay
DOCKER_REGISTRY := ryukinix/$(PROJECT_NAME)
VERSION ?= latest
UID = $(shell id -u)
GID = $(shell id -g)
DOCKER_RUN = docker run $(DOCKER_FLAGS) \
					--user $(UID):$(GID) \
					-e HOME=/tmp --rm \
					-t \
                    -p 8501:8501 \
					-v $(PWD)/tests:/project/tests \
					-w /app

install: # install locally
	python -m venv .venv
	source .venv/bin/activate
	pip install -U pdm setuptools wheel
	pdm install

run: build
	$(DOCKER_RUN) $(PROJECT_NAME)

run-local:
	pdm run streamlit run airdelay/main.py

build:
	docker build -t $(PROJECT_NAME) .

publish: build
	docker tag $(PROJECT_NAME) $(DOCKER_REGISTRY):$(VERSION)
	docker push $(DOCKER_REGISTRY):$(VERSION)

check: build
	$(DOCKER_RUN) $(PROJECT_NAME) check
	sed -i "s|/app|$(PWD)|g" tests/coverage.xml

coverage:
	coverage html
	open htmlcov/index.html

.PHONY: build run run-local check coverage install
