run:
	docker compose up --build -d

test:
	docker compose exec api pytest

stop:
	docker compose down