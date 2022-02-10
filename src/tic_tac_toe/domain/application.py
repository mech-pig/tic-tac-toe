from .data import AddMarkCommand, Game, GameError, Mark


class Application:
    def __init__(self, game: Game) -> None:
        self.game = game

    def add_mark(self, mark: Mark) -> Game | GameError:
        run = AddMarkCommand(mark=mark)
        return run(game=self.game)
