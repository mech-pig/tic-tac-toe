import os
from typing import Mapping
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from tests.fixtures import DRAW, PLAYER_ONE_NEED_TO_START

from tic_tac_toe.adapters.repository.postgres import (
    PostgresGameRepository,
    PostgresGameRepositoryConfig,
)
from tic_tac_toe.domain.application import Application
from tic_tac_toe.domain.data import Cell, Game, GameOngoing, Player
from tic_tac_toe.entrypoints.asgi import create_asgi_app


@pytest.fixture
def make_client():
    async def build(games: Mapping[str, Game]):
        repository = PostgresGameRepository(
            config=PostgresGameRepositoryConfig(
                db_uri=os.environ.get("TEST_POSTGRES_REPOSITORY_DB_URI"),
            )
        )
        for game_id, game in games.items():
            await repository.insert(game_id=game_id, game=game)
        application = Application(repository=repository)
        asgi_app = create_asgi_app(application=application)
        return TestClient(asgi_app)

    return build


def describe_add_mark():
    @pytest.mark.parametrize(
        "game, body, expected",
        [
            pytest.param(
                DRAW,
                {
                    "cell": Cell.BOTTOM_CENTER.value,
                    "player": Player.ONE.value,
                },
                {
                    "error": "GAME_IS_OVER",
                },
                id="game is already over",
            ),
            pytest.param(
                PLAYER_ONE_NEED_TO_START,
                {
                    "cell": Cell.BOTTOM_CENTER.value,
                    "player": Player.TWO.value,
                },
                {
                    "error": "PLAYER_CANT_MOVE",
                    "player": Player.TWO.value,
                },
                id="player is not expected to move",
            ),
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.ONE,
                    marks={
                        Cell.BOTTOM_CENTER: Player.TWO,
                        Cell.TOP_LEFT: Player.ONE,
                    },
                ),
                {
                    "cell": Cell.TOP_LEFT.value,
                    "player": Player.ONE.value,
                },
                {
                    "error": "CELL_ALREADY_MARKED",
                    "cell": Cell.TOP_LEFT.value,
                },
                id="player marks cell already marked by herself",
            ),
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.ONE,
                    marks={
                        Cell.BOTTOM_CENTER: Player.TWO,
                        Cell.TOP_LEFT: Player.ONE,
                    },
                ),
                {
                    "cell": Cell.BOTTOM_CENTER.value,
                    "player": Player.ONE.value,
                },
                {
                    "error": "CELL_ALREADY_MARKED",
                    "cell": Cell.BOTTOM_CENTER.value,
                },
                id="player marks cell already marked by other player",
            ),
        ],
    )
    async def test_domain_error(game, body, expected, make_client):
        game_id = uuid4().hex
        client = await make_client(games={game_id: game})
        response = client.post(f"/games/{game_id}/mark", json=body)
        assert response.status_code == 400
        assert response.json() == expected

    async def test_game_not_found(make_client):
        client = await make_client(games={})
        game_id = "i-dont-exist"
        body = {
            "cell": Cell.BOTTOM_CENTER.value,
            "player": Player.ONE.value,
        }
        expected = {"error": "GAME_NOT_FOUND"}
        response = client.post(f"/games/{game_id}/mark", json=body)
        assert response.status_code == 404
        assert response.json() == expected

    @pytest.mark.parametrize(
        "game, body, expected",
        [
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.ONE,
                    marks={
                        Cell.BOTTOM_CENTER: Player.TWO,
                        Cell.TOP_LEFT: Player.ONE,
                    },
                ),
                {
                    "cell": Cell.CENTER_LEFT.value,
                    "player": Player.ONE.value,
                },
                {
                    "status": "ONGOING",
                    "next_player": Player.TWO.value,
                    "marks": {
                        Cell.BOTTOM_CENTER.value: Player.TWO.value,
                        Cell.TOP_LEFT.value: Player.ONE.value,
                        Cell.CENTER_LEFT.value: Player.ONE.value,
                    },
                },
                id="game is not over",
            ),
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.ONE,
                    marks={
                        Cell.TOP_LEFT: Player.TWO,
                        Cell.TOP_CENTER: Player.ONE,
                        Cell.TOP_RIGHT: Player.TWO,
                        Cell.CENTER_LEFT: Player.ONE,
                        Cell.CENTER_CENTER: Player.ONE,
                        Cell.CENTER_RIGHT: Player.TWO,
                        Cell.BOTTOM_LEFT: Player.TWO,
                        Cell.BOTTOM_CENTER: Player.TWO,
                    },
                ),
                {
                    "cell": Cell.BOTTOM_RIGHT.value,
                    "player": Player.ONE.value,
                },
                {
                    "status": "OVER",
                    "winner": None,
                    "marks": {
                        Cell.TOP_LEFT.value: Player.TWO.value,
                        Cell.TOP_CENTER.value: Player.ONE.value,
                        Cell.TOP_RIGHT.value: Player.TWO.value,
                        Cell.CENTER_LEFT.value: Player.ONE.value,
                        Cell.CENTER_CENTER.value: Player.ONE.value,
                        Cell.CENTER_RIGHT.value: Player.TWO.value,
                        Cell.BOTTOM_LEFT.value: Player.TWO.value,
                        Cell.BOTTOM_CENTER.value: Player.TWO.value,
                        Cell.BOTTOM_RIGHT.value: Player.ONE.value,
                    },
                },
                id="draw",
            ),
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.TWO,
                    marks={
                        Cell.TOP_LEFT: Player.TWO,
                        Cell.TOP_CENTER: Player.ONE,
                        Cell.TOP_RIGHT: Player.TWO,
                        Cell.CENTER_LEFT: Player.ONE,
                        Cell.CENTER_CENTER: Player.TWO,
                        Cell.CENTER_RIGHT: Player.ONE,
                    },
                ),
                {
                    "cell": Cell.BOTTOM_LEFT.value,
                    "player": Player.TWO.value,
                },
                {
                    "status": "OVER",
                    "winner": Player.TWO.value,
                    "marks": {
                        Cell.TOP_LEFT.value: Player.TWO.value,
                        Cell.TOP_CENTER.value: Player.ONE.value,
                        Cell.TOP_RIGHT.value: Player.TWO.value,
                        Cell.CENTER_LEFT.value: Player.ONE.value,
                        Cell.CENTER_CENTER.value: Player.TWO.value,
                        Cell.CENTER_RIGHT.value: Player.ONE.value,
                        Cell.BOTTOM_LEFT.value: Player.TWO.value,
                    },
                },
                id="win",
            ),
        ],
    )
    async def test_success(game, body, expected, make_client):
        game_id = uuid4().hex
        client = await make_client(games={game_id: game})
        response = client.post(f"/games/{game_id}/mark", json=body)
        assert response.status_code == 200
        assert response.json() == expected
