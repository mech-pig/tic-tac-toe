from typing import Callable, Literal, Protocol

from pydantic import BaseModel

from .data import AddMarkCommand, CreateNewGameCommand, Game, GameError, Mark, is_game


class GameNotFound(BaseModel):
    error: Literal["GAME_NOT_FOUND"]


class GameRepository(Protocol):
    async def insert(self, game_id: str, game: Game) -> None:
        ...  # pragma: nocover

    async def get(self, game_id: str) -> Game | GameNotFound:
        ...  # pragma: nocover

    async def update(
        self,
        game_id: str,
        fn: Callable[[Game], Game | GameError],
    ) -> Game | GameError | GameNotFound:
        ...  # pragma: nocover


class GameAggregate(BaseModel):
    id: str
    state: Game


class Application:
    def __init__(
        self,
        repository: GameRepository,
        generate_game_id: Callable[[], str],
    ) -> None:
        self.repository = repository
        self.generate_game_id = generate_game_id

    async def new_game(self) -> GameAggregate:
        create_new_game = CreateNewGameCommand()
        game = create_new_game()
        game_id = self.generate_game_id()
        await self.repository.insert(game_id=game_id, game=game)
        return GameAggregate(id=game_id, state=game)

    async def get_game(self, game_id: str) -> GameAggregate | GameNotFound:
        result = await self.repository.get(game_id=game_id)
        if isinstance(result, GameNotFound):
            return result
        return GameAggregate(id=game_id, state=result)

    async def add_mark(
        self,
        game_id: str,
        mark: Mark,
    ) -> GameAggregate | GameError | GameNotFound:
        result = await self.repository.update(
            game_id=game_id,
            fn=AddMarkCommand(mark=mark),
        )
        if is_game(result):
            return GameAggregate(id=game_id, state=result)
        # type narrowing does not seem to work
        return result  # type: ignore
