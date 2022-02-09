import random

import pytest

from tic_tac_toe.domain.data import (
    WINNING_CELL_COMBINATIONS,
    AddMarkCommand,
    Cell,
    CellAlreadyMarked,
    GameIsOver,
    GameOngoing,
    GameOver,
    Mark,
    Player,
    PlayerCantMove,
)

DRAW = GameOver(
    status="OVER",
    winner=None,
    marks={
        Cell.TOP_LEFT: Player.TWO,
        Cell.TOP_CENTER: Player.ONE,
        Cell.TOP_RIGHT: Player.TWO,
        Cell.CENTER_LEFT: Player.ONE,
        Cell.CENTER_CENTER: Player.ONE,
        Cell.CENTER_RIGHT: Player.TWO,
        Cell.BOTTOM_LEFT: Player.TWO,
        Cell.BOTTOM_CENTER: Player.TWO,
        Cell.BOTTOM_RIGHT: Player.ONE,
    },
)

PLAYER_ONE_WIN = GameOver(
    status="OVER",
    winner=Player.ONE,
    marks={
        Cell.TOP_LEFT: Player.TWO,
        Cell.TOP_CENTER: Player.ONE,
        Cell.TOP_RIGHT: Player.TWO,
        Cell.CENTER_LEFT: Player.ONE,
        Cell.CENTER_CENTER: Player.TWO,
        Cell.BOTTOM_LEFT: Player.TWO,
        Cell.CENTER_RIGHT: Player.ONE,
    },
)

PLAYER_ONE_NEED_TO_START = GameOngoing(
    status="ONGOING",
    next_player=Player.ONE,
    marks={},
)

PLAYER_TWO_NEED_TO_START = GameOngoing(
    status="ONGOING",
    next_player=Player.TWO,
    marks={},
)

PLAYER_ONE_NEED_TO_MOVE = GameOngoing(
    status="ONGOING",
    next_player=Player.ONE,
    marks={
        Cell.TOP_LEFT: Player.TWO,
        Cell.TOP_CENTER: Player.ONE,
    },
)

PLAYER_TWO_NEED_TO_MOVE = GameOngoing(
    status="ONGOING",
    next_player=Player.TWO,
    marks={
        Cell.TOP_LEFT: Player.TWO,
        Cell.TOP_CENTER: Player.ONE,
    },
)


def describe_add_mark():
    @pytest.mark.parametrize(
        "game, mark_to_add",
        [
            pytest.param(
                DRAW,
                Mark(player=Player.ONE, cell=Cell.TOP_CENTER),
                id="draw, player chooses cell marked by herself",
            ),
            pytest.param(
                DRAW,
                Mark(player=Player.ONE, cell=Cell.TOP_LEFT),
                id="draw, player chooses cell marked by other player",
            ),
            pytest.param(
                PLAYER_ONE_WIN,
                Mark(player=Player.ONE, cell=Cell.TOP_CENTER),
                id="winner chooses cell marked by herself",
            ),
            pytest.param(
                PLAYER_ONE_WIN,
                Mark(player=Player.ONE, cell=Cell.TOP_LEFT),
                id="winner chooses cell marked by other player",
            ),
            pytest.param(
                PLAYER_ONE_WIN,
                Mark(player=Player.ONE, cell=Cell.BOTTOM_CENTER),
                id="winner chooses free cell",
            ),
            pytest.param(
                PLAYER_ONE_WIN,
                Mark(player=Player.ONE, cell=Cell.TOP_LEFT),
                id="loser chooses cell marked by herself",
            ),
            pytest.param(
                PLAYER_ONE_WIN,
                Mark(player=Player.ONE, cell=Cell.TOP_CENTER),
                id="loser chooses cell marked by other player",
            ),
            pytest.param(
                PLAYER_ONE_WIN,
                Mark(player=Player.ONE, cell=Cell.BOTTOM_CENTER),
                id="loser chooses free cell",
            ),
        ],
    )
    def test_error_game_is_over(game, mark_to_add):
        assert game.status == "OVER"
        add_mark = AddMarkCommand(mark=mark_to_add)
        expected = GameIsOver(error="GAME_IS_OVER")
        result = add_mark(game=game)
        assert expected == result

    @pytest.mark.parametrize(
        "game, mark_to_add",
        [
            pytest.param(
                PLAYER_TWO_NEED_TO_MOVE,
                Mark(player=Player.ONE, cell=Cell.TOP_CENTER),
                id="player chooses cell marked by herself",
            ),
            pytest.param(
                PLAYER_TWO_NEED_TO_MOVE,
                Mark(player=Player.ONE, cell=Cell.TOP_LEFT),
                id="player chooses cell marked by other player",
            ),
            pytest.param(
                PLAYER_TWO_NEED_TO_MOVE,
                Mark(player=Player.ONE, cell=Cell.BOTTOM_CENTER),
                id="player chooses free cell",
            ),
            pytest.param(
                PLAYER_TWO_NEED_TO_START,
                Mark(player=Player.ONE, cell=Cell.BOTTOM_CENTER),
                id="player starts the game",
            ),
        ],
    )
    def test_error_player_cant_move(game, mark_to_add):
        add_mark = AddMarkCommand(mark=mark_to_add)
        result = add_mark(game=game)
        expected = PlayerCantMove(error="PLAYER_CANT_MOVE", player=mark_to_add.player)
        assert expected == result

    @pytest.mark.parametrize(
        "game, mark_to_add",
        [
            pytest.param(
                PLAYER_TWO_NEED_TO_MOVE,
                Mark(player=Player.TWO, cell=Cell.TOP_LEFT),
                id="player chooses cell marked by herself",
            ),
            pytest.param(
                PLAYER_TWO_NEED_TO_MOVE,
                Mark(player=Player.TWO, cell=Cell.TOP_CENTER),
                id="player chooses cell marked by other player",
            ),
        ],
    )
    def test_error_cell_is_already_marked(game, mark_to_add):
        add_mark = AddMarkCommand(mark=mark_to_add)
        result = add_mark(game=game)
        expected = CellAlreadyMarked(error="CELL_ALREADY_MARKED", cell=mark_to_add.cell)
        assert expected == result

    @pytest.mark.parametrize("winning_cell_index", range(3))
    @pytest.mark.parametrize("winning_combination", WINNING_CELL_COMBINATIONS)
    @pytest.mark.parametrize("winner", list(Player))
    def test_success_game_is_won(winning_combination, winning_cell_index, winner):
        winning_combination_cells = list(winning_combination)
        cell_to_be_marked_by_winner = winning_combination_cells[winning_cell_index]
        cells_already_marked_by_winner = [
            c for c in winning_combination if c != cell_to_be_marked_by_winner
        ]

        defeated = Player.ONE if winner is Player.TWO else Player.TWO
        all_but_winning_combination_cells = [
            c for c in Cell if c not in winning_combination
        ]
        cells_already_marked_by_defeated = random.sample(
            all_but_winning_combination_cells, 2
        )

        game = GameOngoing(
            status="ONGOING",
            next_player=winner,
            marks={
                **{cell: winner for cell in cells_already_marked_by_winner},
                **{cell: defeated for cell in cells_already_marked_by_defeated},
            },
        )
        mark_to_add = Mark(player=winner, cell=cell_to_be_marked_by_winner)
        add_mark = AddMarkCommand(mark=mark_to_add)

        expected = GameOver(
            status="OVER",
            winner=winner,
            marks={**game.marks, cell_to_be_marked_by_winner: winner},
        )
        result = add_mark(game)
        assert expected == result

    def test_success_draw():
        marks = DRAW.marks.copy()
        cell = random.choice(list(marks.keys()))
        player = marks.pop(cell)
        game = GameOngoing(
            status="ONGOING",
            next_player=player,
            marks=marks,
        )
        mark_to_add = Mark(cell=cell, player=player)
        expected = DRAW

        add_mark = AddMarkCommand(mark=mark_to_add)
        result = add_mark(game=game)
        assert result == expected

    @pytest.mark.parametrize(
        "game, mark_to_add",
        [
            pytest.param(
                PLAYER_ONE_NEED_TO_START,
                Mark(cell=Cell.CENTER_CENTER, player=Player.ONE),
                id="player one marks first cell",
            ),
            pytest.param(
                PLAYER_TWO_NEED_TO_START,
                Mark(cell=Cell.CENTER_CENTER, player=Player.TWO),
                id="player two marks first cell",
            ),
            pytest.param(
                PLAYER_ONE_NEED_TO_MOVE,
                Mark(cell=Cell.CENTER_CENTER, player=Player.ONE),
                id="player one adds mark",
            ),
            pytest.param(
                PLAYER_TWO_NEED_TO_MOVE,
                Mark(cell=Cell.CENTER_CENTER, player=Player.TWO),
                id="player two adds mark",
            ),
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.ONE,
                    marks={
                        Cell.TOP_LEFT: Player.TWO,
                        Cell.CENTER_CENTER: Player.ONE,
                        Cell.TOP_CENTER: Player.TWO,
                    },
                ),
                Mark(cell=Cell.BOTTOM_LEFT, player=Player.ONE),
                id="player one avoids defeat",
            ),
            pytest.param(
                GameOngoing(
                    status="ONGOING",
                    next_player=Player.TWO,
                    marks={
                        Cell.TOP_LEFT: Player.ONE,
                        Cell.CENTER_CENTER: Player.TWO,
                        Cell.TOP_CENTER: Player.ONE,
                    },
                ),
                Mark(cell=Cell.BOTTOM_LEFT, player=Player.TWO),
                id="player two avoids defeat",
            ),
        ],
    )
    def test_success_ongoing(game, mark_to_add):
        assert game.status == "ONGOING"
        expected = GameOngoing(
            status="ONGOING",
            next_player=Player.ONE if game.next_player == Player.TWO else Player.TWO,
            marks={**game.marks, mark_to_add.cell: mark_to_add.player},
        )
        add_mark = AddMarkCommand(mark=mark_to_add)
        result = add_mark(game=game)
        assert expected == result
