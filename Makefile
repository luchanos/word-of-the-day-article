local_file = "docker-compose-ci.yaml"
test_file = "docker-compose-test.yaml"

up:
	docker compose -f $(local_file) up -d

down:
	docker compose -f $(local_file) down

recreate:
	docker compose -f $(local_file) up -d --build --force-recreate

build_test:
	docker compose -f $(test_file) build

run_tests:
	docker compose -f $(test_file) run --rm web

down_test:
	docker compose -f $(test_file) down