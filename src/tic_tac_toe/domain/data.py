from enum import Enum
from typing import Annotated, Literal, Mapping, Optional

from pydantic import BaseModel, Field


class Player(Enum):
    ONE = 1
    TWO = 2


class Cell(Enum):
    TOP_LEFT = "TOP_LEFT"
    TOP_CENTER = "TOP_CENTER"
    TOP_RIGHT = "TOP_RIGHT"
    CENTER_LEFT = "CENTER_LEFT"
    CENTER_CENTER = "CENTER_CENTER"
    CENTER_RIGHT = "CENTER_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_CENTER = "BOTTOM_CENTER"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


WINNING_CELL_COMBINATIONS = frozenset(
    [
        frozenset([Cell.TOP_LEFT, Cell.TOP_CENTER, Cell.TOP_RIGHT]),
        frozenset([Cell.CENTER_LEFT, Cell.CENTER_CENTER, Cell.CENTER_RIGHT]),
        frozenset([Cell.BOTTOM_LEFT, Cell.BOTTOM_CENTER, Cell.BOTTOM_RIGHT]),
        frozenset([Cell.TOP_LEFT, Cell.CENTER_LEFT, Cell.BOTTOM_LEFT]),
        frozenset([Cell.TOP_CENTER, Cell.CENTER_CENTER, Cell.BOTTOM_CENTER]),
        frozenset([Cell.TOP_RIGHT, Cell.CENTER_RIGHT, Cell.BOTTOM_RIGHT]),
        frozenset([Cell.TOP_LEFT, Cell.CENTER_CENTER, Cell.BOTTOM_RIGHT]),
        frozenset([Cell.BOTTOM_LEFT, Cell.CENTER_CENTER, Cell.TOP_RIGHT]),
    ]
)

BoardMarks = Mapping[Cell, Player]


class Mark(BaseModel):
    player: Player
    cell: Cell


class GameOngoing(BaseModel):
    status: Literal["ONGOING"]
    next_player: Player
    marks: BoardMarks


class GameOver(BaseModel):
    status: Literal["OVER"]
    winner: Optional[Player]
    marks: BoardMarks


Game = Annotated[
    GameOngoing | GameOver,
    Field(discriminator="status"),
]


class CellAlreadyMarked(BaseModel):
    error: Literal["CELL_ALREADY_MARKED"]
    cell: Cell


class PlayerCantMove(BaseModel):
    error: Literal["PLAYER_CANT_MOVE"]
    player: Player


class GameIsOver(BaseModel):
    error: Literal["GAME_IS_OVER"]


GameError = Annotated[
    CellAlreadyMarked | GameIsOver | PlayerCantMove,
    Field(discriminator="error"),
]


class AddMarkCommand(BaseModel):
    mark: Mark

    def __call__(self, game: Game) -> Game | GameError:
        if isinstance(game, GameOver):
            return GameIsOver(error="GAME_IS_OVER")
        if game.next_player != self.mark.player:
            return PlayerCantMove(error="PLAYER_CANT_MOVE", player=self.mark.player)
        if self.mark.cell in game.marks:
            return CellAlreadyMarked(error="CELL_ALREADY_MARKED", cell=self.mark.cell)

        updated_marks = {**game.marks, self.mark.cell: self.mark.player}
        cells_marked_by_player = frozenset(
            [
                cell
                for cell, player in updated_marks.items()
                if player == self.mark.player
            ]
        )
        winning_combinations_to_check = frozenset(
            [
                combination
                for combination in WINNING_CELL_COMBINATIONS
                if self.mark.cell in combination
            ]
        )

        is_player_winner = any(
            (
                combination.issubset(cells_marked_by_player)
                for combination in winning_combinations_to_check
            )
        )

        if is_player_winner:
            return GameOver(
                status="OVER",
                winner=self.mark.player,
                marks=updated_marks,
            )

        if updated_marks.keys() == set(Cell):
            return GameOver(
                status="OVER",
                winner=None,
                marks=updated_marks,
            )

        return GameOngoing(
            status="ONGOING",
            next_player=Player.ONE if game.next_player == Player.TWO else Player.TWO,
            marks=updated_marks,
        )
