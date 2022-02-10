ENV_VARS = \
	HTTP_PORT=8080

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
	poetry run pytest $(PYTEST_ARGS)