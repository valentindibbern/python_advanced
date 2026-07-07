from src.Classes.Game import GameResponse


class Scene:
    def __init__(self, scene_id: int, scene_name: str) -> None:
        self.scene_id: int = scene_id
        self.scene_name: str = scene_name

    def start(self) -> GameResponse:
        ...

    def handle_text_input(self, text: str) -> GameResponse:
        ...

    def handle_choice(self, choice_id: str) -> GameResponse:
        ...