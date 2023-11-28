.PHONY: start stop build sh tsh ash logs test atest embed-all embed-first restart config commit lint psql migrate rollback tpsql tmigrate trollback demo-data promote load-products-sample load-products

# \
!ifndef 0 # \
test_env_setting="DATABASE_URL=$$TEST_DATABASE_URL" # \
!else
test_env_setting=DATABASE_URL=\$$TEST_DATABASE_URL
# \
!endif

container=fresh-cart-be
fecontainer=fresh-cart-fe

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
	docker compose exec -T $(fecontainer) /bin/sh -c "npm test"

# get a shell within the app container
sh:
	docker compose exec $(container) /bin/sh

tsh:
	docker compose exec $(container) /bin/sh -c "$(test_env_setting) sh"

ash:
	docker compose exec $(fecontainer) /bin/sh

embed-all:
	docker compose exec $(container) /bin/sh -c "poetry run embed --all"

embed-first:
	docker compose exec $(container) /bin/sh -c "poetry run embed --first"

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
	docker compose exec $(container) poetry run autoflake --remove-all-unused-imports --in-place --recursive freshcart migrations
	docker compose exec $(container) poetry run isort freshcart migrations
	docker compose exec $(container) poetry run black freshcart migrations

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

load-products-sample:
	docker compose exec postgres psql -U app_dev dev -f /db/products-sample.sql

load-products:
	docker compose exec postgres psql -U app_dev dev -f /db/products.sql

app-logs:
	docker compose exec $(container) /bin/sh -c "tail -f /var/log/fresh-cart.log"

reset-app-logs:
	docker compose exec $(container) /bin/sh -c "echo -ne "" > /var/log/fresh-cart.log"