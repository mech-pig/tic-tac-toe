from typing import Callable, Literal, Protocol

from pydantic import BaseModel

from .data import AddMarkCommand, Game, GameError, Mark


class GameNotFound(BaseModel):
    error: Literal["GAME_NOT_FOUND"]


class GameRepository(Protocol):
    async def update(
        self,
        game_id: str,
        fn: Callable[[Game], Game | GameError],
    ) -> Game | GameError | GameNotFound:
        ...  # pragma: nocover


class Application:
    def __init__(self, repository: GameRepository) -> None:
        self.repository = repository

    async def add_mark(
        self,
        game_id: str,
        mark: Mark,
    ) -> Game | GameError | GameNotFound:
        return await self.repository.update(
            game_id=game_id,
            fn=AddMarkCommand(mark=mark),
        )
