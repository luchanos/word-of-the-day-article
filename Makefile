local_file = "docker-compose-local.yaml"

up_local_compose:
	docker compose -f $(local_file) up -d

down_local_compose:
	docker compose -f $(local_file) down

recreate_local_compose:
	docker compose -f $(local_file) up -d --build --force-recreate