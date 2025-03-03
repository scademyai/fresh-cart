# fresh-cart
An AI-driven application used in SCADEMY's AI courses

# how to build

1. Copy `.env.sample` to `.env`
```bash
cp .env.sample .env
```
2. Obtain `OPENAI_API_KEY` from the KeePassX db. Its name is *OpenAI API key for AI course*
3. Add it to `.env`

# how to add Angular dependencies

- Navigate to `/client` and install dependencies there.
- Use `yarn` to install new ones.

# prerequisites for development
- [Docker](https://docs.docker.com/engine/install/)

Once you have these installed, you are all set. All development happens within the container.

`Dockerfile` describes the container for the app. `docker-compose.yml` describes the environment outside of the app container, like DBs, queues, etc.

# how to run
Using `make`. Check out the `Makefile`.

For Windows, there is [NMake](https://docs.microsoft.com/en-us/cpp/build/reference/nmake-reference?view=vs-2019).
Or you may use [make for windows](https://sourceforge.net/projects/gnuwin32/).


Create `fresh-cart.log` in the root directory of this repo first.

```
make start
```

# how to execute tests

Prerequisites

```bash
make build
make start
make tmigrate
```
To run all tests
```bash
make test
``` 

To run a specific test class
```bash
make sh
poetry run nose2 -v tests.api.platform.portal.api_test
```
Path is the relative path of the file, `/` replaced with `.` and file extension is removed (.py).

To run a specific test case
```bash
make sh
poetry run nose2 -v tests.api.platform.portal.api_test.TestPortalApi.test_get_participant_portal_config_returns_correct_data
```
The path is same as before, test class and method is appended.


## get nmake.exe
Download `Build Tools for Visual Studio 2019` from [Microsoft's VS site](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019). Install only `MSVC ... build tools ` under `C++ build tools`.

# dependencies
Dependencies are managed via `poetry`. To manage dependencies always connect to the container (`make sh`) and run poetry within.

To add a new package use `poetry add [package-name]`.

# database
The project uses Postgresql w/ SQLAlchemy as an ORM and Alembic.

Migrations are stored under `migrations/versions`

## to reset the db
Before reseting, stop the containers with `make stop`. To get a completely clean postgres DB, you need to delete the `fresh-cart_pgdata` docker volume.

## to get a db console
```
make psql
make tpsql # for test db
```

## to migrate to the latest schema
```
make migrate
make tmigrate # for test db
```

## to rollback one migration
```
make rollback
make trollback # for test db
```

## to create a new migration
Use autogenerated migrations by editing the model first, and then running the below script.

```
make sh
poetry run alembic revision --autogenerate -m "[description]"
```

Adjust the generated migration if needed.

### to check a migration
```
make sh
poetry run alembic upgrade --sql head
```

# commit messages
Follow [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/#summary) messages. This will allow us to automatically generate changelogs and versioning.
