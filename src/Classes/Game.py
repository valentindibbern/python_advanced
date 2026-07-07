from src.Datatypes.Enums import  State
from src.Classes.Player import Player
from src.Classes.Scene import Scene
from src.Datatypes.Models import GameResponse
from src.Scenes.scene1.scene import CharacterCreationScene
from src.Scenes.scene2.scene import BallroomArrivalScene


class Game:
    def __init__(self) -> None:
        self.state: State = State.START
        self.player: Player = Player()
        self.current_scene_id: int = 0
        self.current_scene: Scene = self._load_scene(self.current_scene_id)
        self.story_flags: dict[str, str] = {}

    def start(self) -> GameResponse:
        return self.current_scene.start()

    def handle_text_input(self, text: str) -> GameResponse:
        response = self.current_scene.handle_text_input(text)
        return self._save_scene_progress(response)

    def handle_choice(self, choice_id: str) -> GameResponse:
        response = self.current_scene.handle_choice(choice_id)
        return self._save_scene_progress(response)

    def _save_scene_progress(self, response: GameResponse) -> GameResponse:
        if self.current_scene is None:
            return response

        if self.current_scene.is_done():
            self.player = self.current_scene.get_player()
            self.state = State.SCENE_COMPLETE
            return self._start_next_scene()

        return response

    def _start_next_scene(self) -> GameResponse:
        self.current_scene_id += 1
        self.current_scene = self._load_scene(self.current_scene_id)
        return self.current_scene.start()

        return response

    def _load_scene(self, scene_id: int) -> Scene:
        match scene_id:
            case 0:
                return CharacterCreationScene(scene_id, "CharacterCreationScene")
            case 1:
                return BallroomArrivalScene(scene_id, "BallroomArrivalScene", self.player, self.story_flags)

        raise ValueError(f"Szene {scene_id} ist nicht bekannt.")
