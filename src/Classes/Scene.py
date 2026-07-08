from src.Classes.Player import Player
from src.Datatypes.Models import GameResponse


class Scene:
    def __init__(self, scene_id: int, player: Player) -> None:
        self.scene_id: int = scene_id
        self.player: Player = player

    def start(self) -> GameResponse:
        raise NotImplementedError("Szenen müssen start() implementieren.")

    def handle_text_input(self, text: str) -> GameResponse:
        raise NotImplementedError("Szenen müssen handle_text_input() implementieren.")

    def handle_choice(self, choice_id: str) -> GameResponse:
        raise NotImplementedError("Szenen müssen handle_choice() implementieren.")

    def is_done(self) -> bool:
        raise NotImplementedError("Szenen müssen is_done() implementieren.")

    def get_player(self) -> Player:
        raise NotImplementedError("Szenen müssen get_player() implementieren.")
