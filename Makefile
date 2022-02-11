POSTGRES_USER = "tic-tac-toe"
POSTGRES_PASSWORD = "supersecret"
POSTGRES_DATABASE = "tic-tac-toe"

ENV_VARS = \
	HTTP_PORT=8080 \
	POSTGRES_REPOSITORY_DB_URI="postgres://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@localhost:5432/$(POSTGRES_DATABASE)"

CTX_ENV_VARS = \
	POSTGRES_DATABASE=$(POSTGRES_DATABASE) \
	POSTGRES_USER=$(POSTGRES_USER) \
	POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)

TEST_ENV_VARS = \
	TEST_POSTGRES_REPOSITORY_DB_URI="postgres://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@localhost:5432/$(POSTGRES_DATABASE)"

PYTEST_ARGS = src tests


.PHONY: dev
dev:
	$(ENV_VARS) poetry run gunicorn --reload "tic_tac_toe.__main__:asgi()"


.PHONY: install-dev
install-dev:
	poetry install


.PHONY: check
check: check-style check-types check-fmt


.PHONY: check-style
check-style:
	poetry run flake8 src


.PHONY: check-types
check-types:
	poetry run mypy


.PHONY: check-fmt
check-fmt:
	poetry run black src --check


.PHONY: fmt
fmt:
	poetry run black src


.PHONY: test
test:
	@$(TEST_ENV_VARS) poetry run pytest $(PYTEST_ARGS)


.PHONY: ctx-up
ctx-up:
	@$(CTX_ENV_VARS) docker-compose up -d


.PHONY: ctx-down
ctx-down:
	@$(CTX_ENV_VARS) docker-compose down


.PHONY: ctx-logs
ctx-logs:
	@$(CTX_ENV_VARS) docker-compose logs -f


.PHONY: ctx-migrations-deploy
ctx-migrations-deploy:
	@$(CTX_ENV_VARS) docker-compose run postgres-migrations deploy