docker-spin-up:
	docker-compose --env-file .env up --build -d

down:
	docker-compose down

pytest:
	docker container exec load pytest /code/tests