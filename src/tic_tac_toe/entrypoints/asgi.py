from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tic_tac_toe.domain.application import Application
from tic_tac_toe.domain.data import Game, GameError, Mark, is_game


def create_asgi_app(application: Application) -> FastAPI:

    api = FastAPI()

    @api.post(
        "/games/{game_id}/mark",
        # not sure why, but Annotated models seems to cause errors
        # ignoring typecheck for now
        response_model=Game,  # type: ignore
        responses={status.HTTP_400_BAD_REQUEST: {"model": GameError}},
    )
    def add_mark(game_id: str, mark: Mark) -> Game | JSONResponse:
        result = application.add_mark(mark=mark)
        if is_game(result):
            return result
        return JSONResponse(
            content=jsonable_encoder(result),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return api
