from src.Classes.Player import Player
from src.Datatypes.Models import GameResponse


class Scene:
    def __init__(self, scene_id: int, player: Player) -> None:
        self.scene_id: int = scene_id
        self.player: Player = player

    def start(self) -> GameResponse:
        ...

    def handle_text_input(self, text: str) -> GameResponse:
        ...

    def handle_choice(self, choice_id: str) -> GameResponse:
        ...

    def is_done(self) -> bool:
        ...

    def get_player(self) -> Player:
        ...
