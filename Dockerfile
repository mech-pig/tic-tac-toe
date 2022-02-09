FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR="/var/cache/pypoetry"

WORKDIR /home/tictactoe


RUN pip install --no-cache poetry && poetry --version

COPY ./poetry.lock ./pyproject.toml /home/tictactoe/

# install production dependencies
RUN poetry install --no-interaction --no-dev --no-ansi --no-root \
    && rm -rf ${POETRY_CACHE_DIR}

COPY ./src/ /home/tictactoe/src/
COPY ./gunicorn.conf.py /home/tictactoe/gunicorn.conf.py

# install root package
RUN poetry install --no-interaction --no-dev --no-ansi \
    && rm -rf ${POETRY_CACHE_DIR}

# run as non-root user
RUN groupadd -r web \
    && useradd -d /home/tictactoe -r -g web tictactoe \
    && chown tictactoe:web -R /home/tictactoe

USER tictactoe

EXPOSE 8080

ENV HTTP_PORT=8080

ENTRYPOINT [ "poetry", "run", "gunicorn", "tictactoe.entrypoints.asgi:create_app()" ]
