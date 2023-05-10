.PHONY: start stop build sh tsh logs test atest restart config commit lint psql migrate rollback tpsql tmigrate trollback demo-data promote

# \
!ifndef 0 # \
test_env_setting="DATABASE_URL=$$TEST_DATABASE_URL" # \
!else
test_env_setting=DATABASE_URL=\$$TEST_DATABASE_URL
# \
!endif

container=fresh-cart

# start all the containers
start:
	docker compose up -d

# stop all the containers
stop:
	docker compose down

# restart containers
restart: stop start

# build the app container
build:
	docker compose build

# run tests
test:
	docker compose exec -T $(container) /bin/sh -c "$(test_env_setting) poetry run nose2 -v"

atest:
	docker compose exec -T $(container) /bin/sh -c "yarn --cwd client test"

# get a shell within the app container
sh:
	docker compose exec $(container) /bin/sh

tsh:
	docker compose exec $(container) /bin/sh -c "$(test_env_setting) sh"

# check console output
logs:
	docker compose logs -f

# show the combined compose file used
config:
	docker compose config

# commit using commitizen
commit:
	docker compose exec $(container) poetry run cz c

# lint code
lint:
	docker compose exec $(container) poetry run autoflake --remove-all-unused-imports --in-place --recursive app.py lib migrations scripts tests
	docker compose exec $(container) poetry run isort app.py lib migrations scripts tests
	docker compose exec $(container) poetry run black app.py lib migrations scripts tests

# console to the DB
psql:
	docker compose exec postgres psql -U app_dev dev

tpsql:
	docker compose exec postgres psql -U app_test test

# run all migrations
migrate:
	docker compose exec $(container) poetry run alembic upgrade head

tmigrate:
	docker compose exec $(container) /bin/sh -c "$(test_env_setting) poetry run alembic upgrade head"

rollback:
	docker compose exec $(container) poetry run alembic downgrade -1

trollback:
	docker compose exec $(container) /bin/sh -c "$(test_env_setting) poetry run alembic downgrade -1"
