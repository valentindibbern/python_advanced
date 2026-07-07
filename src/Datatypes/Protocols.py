from typing import Protocol

from Classes.Game import GameResponse
from Classes.PC import PC


class GameScene(Protocol):
    def start(self) -> GameResponse:
        ...

    def handle_text_input(self, text: str) -> GameResponse:
        ...

    def handle_choice(self, choice_id: str) -> GameResponse:
        ...

    def is_done(self) -> bool:
        ...

    def get_player(self) -> PC | None:
        ...
