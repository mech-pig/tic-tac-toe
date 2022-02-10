from tic_tac_toe.domain.data import Cell, GameOngoing, GameOver, Player

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

PLAYER_TWO_WIN = GameOver(
    status="OVER",
    winner=Player.TWO,
    marks={
        Cell.TOP_LEFT: Player.TWO,
        Cell.TOP_CENTER: Player.ONE,
        Cell.TOP_RIGHT: Player.TWO,
        Cell.CENTER_LEFT: Player.ONE,
        Cell.CENTER_CENTER: Player.TWO,
        Cell.CENTER_RIGHT: Player.ONE,
        Cell.BOTTOM_LEFT: Player.TWO,
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
