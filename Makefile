docker-spin-up:
	docker compose --env-file .env up --build -d

down:
	docker compose --env-file .env down

shell-load:
	docker container exec -it load_crypto bash

shell-transform:
	docker container exec -it transform_crypto bash

format-load:
	docker container exec load_crypto python -m black -S --line-length 79 .

format-transform:
	docker container exec transform_crypto python -m black -S --line-length 79 .

isort-load:
	docker container exec load_crypto isort .

isort-transform:
	docker container exec transform_crypto isort .

pytest:
	docker container exec load_crypto pytest /code/tests

type-load:
	docker container exec load_crypto mypy --ignore-missing-imports /code

type-transform:
	docker container exec transform_crypto mypy --ignore-missing-imports /code

lint-load:
	docker container exec load_crypto flake8 /code

lint-transform:
	docker container exec transform_crypto flake8 /code

ci-load:
	isort-load format-load type-load lint-load pytest

ci-transform:
	isort-transform format-transform type-transform lint-transform pytest

stop-load-etl:
	docker container exec load_crypto service cron stop

stop-transform-etl:
	docker container exec transform_crypto service cron stop

##########################################################

tf-init:
	terraform -chdir=./terraform init

infra-up-plan:
	terraform -chdir=./terraform plan

infra-up:
	terraform -chdir=./terraform apply

infra-down:
	terraform -chdir=./terraform destroy