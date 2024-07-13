local_file = "docker-compose-ci.yaml"

up:
	docker compose -f $(local_file) up -d

down:
	docker compose -f $(local_file) down

recreate:
	docker compose -f $(local_file) up -d --build --force-recreate