start:
	docker-compose up -d

stop:
	docker-compose down

fake:
	docker-compose exec api python -m app.faker
