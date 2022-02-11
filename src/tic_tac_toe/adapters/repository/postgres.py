import json
from functools import partial
from typing import Callable

from fastapi.encoders import jsonable_encoder
from psycopg import AsyncConnection
from psycopg.types.json import Jsonb, set_json_dumps
from pydantic import BaseModel, PostgresDsn

from tic_tac_toe.domain.application import GameNotFound, GameRepository
from tic_tac_toe.domain.data import Game, GameError, GameOngoing, GameOver, is_game

# https://www.psycopg.org/psycopg3/docs/basic/adapt.html#json-adaptation
set_json_dumps(partial(json.dumps, default=jsonable_encoder))


class PostgresGameRepositoryConfig(BaseModel):
    db_uri: PostgresDsn


class PostgresGameRepository(GameRepository):
    def __init__(self, config: PostgresGameRepositoryConfig):
        self.db_uri = config.db_uri

    async def insert(self, game_id: str, game: Game) -> None:
        async with await AsyncConnection.connect(self.db_uri) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO game (id, state)
                    VALUES (%(id)s, %(state)s)
                    """,
                    {"id": game_id, "state": Jsonb(game)},
                )

    async def get(self, game_id: str) -> Game | GameNotFound:
        async with await AsyncConnection.connect(self.db_uri) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                        SELECT state FROM game
                        WHERE id = %(id)s
                        """,
                    {"id": game_id},
                )
                row = await cursor.fetchone()
                if row is None:
                    return GameNotFound(error="GAME_NOT_FOUND")

                game_data = row[0]

                game: Game = (
                    GameOngoing(**game_data)
                    if game_data["status"] == "ONGOING"
                    else GameOver(**game_data)
                )
                return game

    async def update(
        self,
        game_id: str,
        fn: Callable[[Game], Game | GameError],
    ) -> Game | GameError | GameNotFound:
        async with await AsyncConnection.connect(self.db_uri) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT state FROM game
                    WHERE id = %(id)s
                    FOR UPDATE
                    """,
                    {"id": game_id},
                )
                row = await cursor.fetchone()
                if row is None:
                    return GameNotFound(error="GAME_NOT_FOUND")

                game_data = row[0]

                game: Game = (
                    GameOngoing(**game_data)
                    if game_data["status"] == "ONGOING"
                    else GameOver(**game_data)
                )
                result = fn(game)
                if is_game(result):
                    await cursor.execute(
                        """
                        UPDATE game
                        SET state = %(state)s
                        WHERE id = %(id)s
                        """,
                        {"id": game_id, "state": Jsonb(game)},
                    )
                return result
