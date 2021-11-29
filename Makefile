# ViennaRNA container must be built first, so we remove it from the list; then prepend it.

all: create_local_config fetch_python_requirements build_dockers run_tests

create_local_config:
	@echo "CREATING LOCAL CONFIG FILE"
	cp config.json -n config_local.json  # Shouldn't overwrite existing local config

fetch_python_requirements:
	@echo "FETCHING PYTHON REQUIREMENTS"
	pip install -r requirements.txt

build_dockers:
	@echo "BUILDING DOCKERS"
	docker-compose up --build --no-start

run_tests:
	@echo "RUNNING TESTS"
	python3 test.py

