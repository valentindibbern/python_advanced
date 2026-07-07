from src.Datatypes.Protocols import GameScene
from src.Datatypes.Enums import  State
from src.Classes.PC import PC
from src.Datatypes.Models import GameResponse
from src.Scenes.scene0.scene import CharacterCreationScene
from src.Scenes.scene1.scene import BallroomArrivalScene


class Game:
    def __init__(self) -> None:
        self.state: State = State.START
        self.player: PC | None = None
        self.current_scene: GameScene | None = None
        self.current_scene_id: str = "scene0"
        self.story_flags: dict[str, str] = {}

    # Läd Szene scene1
    # TODO
    def start(self) -> GameResponse:
        self.current_scene = self._load_scene(self.current_scene_id)
        self.state = State.CHARACTER_CREATION
        return self.current_scene.start()

    def handle_text_input(self, text: str) -> GameResponse:
        if self.current_scene is None:
            return self.start()

        response = self.current_scene.handle_text_input(text)
        return self._save_scene_progress(response)

    def handle_choice(self, choice_id: str) -> GameResponse:
        if self.current_scene is None:
            return self.start()

        response = self.current_scene.handle_choice(choice_id)
        return self._save_scene_progress(response)

    def _save_scene_progress(self, response: GameResponse) -> GameResponse:
        if self.current_scene is None:
            return response

        if self.current_scene.is_done():
            self.player = self.current_scene.get_player()
            self.state = State.SCENE_COMPLETE
            return self._start_next_scene(response)

        return response

    def _start_next_scene(self, response: GameResponse) -> GameResponse:
        if self.current_scene_id == "scene0":
            self.current_scene_id = "scene1"
            self.current_scene = self._load_scene(self.current_scene_id)
            self.state = State.TALKING
            return self.current_scene.start()

        return response

    def _load_scene(self, scene_id: str) -> GameScene:
        if scene_id == "scene0":
            return CharacterCreationScene(scene_id, "CharacterCreationScene")

        if scene_id == "scene1":
            return BallroomArrivalScene(scene_id, "BallroomArrivalScene", self.player, self.story_flags)

        raise ValueError(f"Szene {scene_id} ist nicht bekannt.")
