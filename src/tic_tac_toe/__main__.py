import os

from fastapi import FastAPI
from pydantic import PostgresDsn

from tic_tac_toe.adapters.repository.postgres import (
    PostgresGameRepository,
    PostgresGameRepositoryConfig,
)
from tic_tac_toe.domain.application import Application
from tic_tac_toe.entrypoints.asgi import create_asgi_app


def asgi() -> FastAPI:
    db_uri: PostgresDsn = os.getenv("POSTGRES_REPOSITORY_DB_URI")  # type: ignore
    config = PostgresGameRepositoryConfig(db_uri=db_uri)
    repository = PostgresGameRepository(config=config)
    application = Application(repository=repository)
    return create_asgi_app(application=application)
