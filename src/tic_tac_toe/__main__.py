from fastapi import FastAPI

from tic_tac_toe.domain.application import Application
from tic_tac_toe.domain.data import Cell, GameOngoing, Player
from tic_tac_toe.entrypoints.asgi import create_asgi_app


def asgi() -> FastAPI:
    game = GameOngoing(
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
    )
    application = Application(game=game)
    return create_asgi_app(application=application)
