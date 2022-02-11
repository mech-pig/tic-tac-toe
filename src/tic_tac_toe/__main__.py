import os
from uuid import uuid4

from fastapi import FastAPI
from pydantic import PostgresDsn

from tic_tac_toe.adapters.repository.postgres import (
    PostgresGameRepository,
    PostgresGameRepositoryConfig,
)
from tic_tac_toe.domain.application import Application
from tic_tac_toe.entrypoints.asgi import create_asgi_app


def generate_game_id() -> str:
    return uuid4().hex


def asgi() -> FastAPI:
    db_uri: PostgresDsn = os.getenv("POSTGRES_REPOSITORY_DB_URI")  # type: ignore
    config = PostgresGameRepositoryConfig(db_uri=db_uri)
    repository = PostgresGameRepository(config=config)
    application = Application(
        repository=repository,
        generate_game_id=generate_game_id,
    )
    return create_asgi_app(application=application)
