import importlib.util
from pathlib import Path
from typing import Protocol, TypedDict

from src.Classes.PC import PC
from src.Classes.Scene import Choice
from src.Enums.Attributes import Attributes
from src.Enums.State import State
from src.Enums.InputMode import InputMode


class CharacterData(TypedDict, total=False):
    name: str
    species: str
    player_class: str
    knowledge: int
    wit: int
    understanding: int
    goal: str


class GameResponse(TypedDict):
    text: str
    input_mode: InputMode
    choices: list[Choice]
    character: CharacterData | None
    is_finished: bool


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


class Game:
    def __init__(self) -> None:
        self.state: State = State.START
        self.player: PC | None = None
        self.current_scene: GameScene | None = None
        self.current_scene_id: str = "0"
        self.story_flags: dict[str, str] = {}

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

    def _make_response(
        self,
        text: str,
        input_mode: InputMode = InputMode.NONE,
        choices: list[Choice] | None = None,
        character: CharacterData | None = None,
        is_finished: bool = False,
    ) -> GameResponse:
        return {
            "text": text,
            "input_mode": input_mode,
            "choices": choices or [],
            "character": character,
            "is_finished": is_finished,
        }

    def _get_character_data(self) -> CharacterData | None:
        if self.player is None:
            return None

        attributes = self.player.attributes
        return {
            "name": self.player.name,
            "species": self.player.species.get_label() if self.player.species is not None else "-",
            "player_class": self.player.player_class.get_label()
            if self.player.player_class is not None
            else "-",
            "knowledge": attributes.get(Attributes.KNOWLEDGE, 0),
            "wit": attributes.get(Attributes.WIT, 0),
            "understanding": attributes.get(Attributes.UNDERSTANDING, 0),
            "goal": "-",
        }

    def _save_scene_progress(self, response: GameResponse) -> GameResponse:
        if self.current_scene is None:
            return response

        if self.current_scene.is_done():
            self.player = self.current_scene.get_player()
            self.state = State.SCENE_COMPLETE
            return self._start_next_scene(response)

        return response

    def _start_next_scene(self, response: GameResponse) -> GameResponse:
        if self.current_scene_id == "0":
            self.current_scene_id = "1"
            self.current_scene = self._load_scene(self.current_scene_id)
            self.state = State.TALKING
            return self.current_scene.start()

        return response

    def _load_scene(self, scene_id: str) -> GameScene:
        scene_path = self._get_scene_path(scene_id)
        spec = importlib.util.spec_from_file_location(f"scene_{scene_id}", scene_path)

        if spec is None or spec.loader is None:
            raise FileNotFoundError(f"Szene {scene_id} konnte nicht geladen werden.")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if scene_id == "0":
            return module.CharacterCreationScene()

        if scene_id == "1":
            if self.player is None:
                raise ValueError("Szene 1 braucht einen fertigen Charakter.")
            return module.BallroomArrivalScene(self.player, self.story_flags)

        raise ValueError(f"Szene {scene_id} ist nicht bekannt.")

    def _get_scene_path(self, scene_id: str) -> Path:
        project_root = Path(__file__).parents[2]
        possible_paths = [
            project_root / "Scenes" / scene_id / "scene.py",
            project_root / "src" / "Scenes" / scene_id / "scene.py",
        ]

        for scene_path in possible_paths:
            if scene_path.exists():
                return scene_path

        raise FileNotFoundError(f"Szene {scene_id} konnte nicht gefunden werden.")
