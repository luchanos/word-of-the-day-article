local_file = "docker-compose-ci.yaml"
test_file = "docker-compose-test.yaml"

# Define a special target .PHONY to avoid conflicts with files named 'help'
.PHONY: help up down recreate build_tests run_tests down_tests lint format

# Help target
help:
	@echo "Available commands:"
	@echo ""
	@awk 'BEGIN {FS = ":.*#"; printf "  %-20s %s\n", "Command", "Description"; printf "  %-20s %s\n", "-------", "-----------";} /^[a-zA-Z_-]+:.*?#/ { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# Commands
up: # Start the application using docker-compose-ci.yaml
	docker compose -f $(local_file) up -d

down: # Stop the application using docker-compose-ci.yaml
	docker compose -f $(local_file) down

recreate: # Recreate the application containers using docker-compose-ci.yaml
	docker compose -f $(local_file) up -d --build --force-recreate

build_tests: # Build the test Docker image using docker-compose-test.yaml
	docker compose -f $(test_file) build

run_tests: # Run tests using the test Docker image and docker-compose-test.yaml
	docker compose -f $(test_file) run --rm web

down_tests: # Stop the test containers using docker-compose-test.yaml
	docker compose -f $(test_file) down

lint: # Run linters (black, isort, flake8) to check code formatting and quality
	black --check .
	isort --check-only .
	flake8 .

format: # Automatically format code using black and isort
	black .
	isort .