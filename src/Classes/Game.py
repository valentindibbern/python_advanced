from src.Utils import make_response
from src.Datatypes.Enums import InputMode, State
from src.Classes.Player import Player
from src.Classes.Scene import Scene
from src.Datatypes.Models import GameMsgType, GameResponse, UiMsgType, UiResponse
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
        ui_response: UiResponse = {
            "msg_id": "ui-start",
            "msg_type": UiMsgType.START,
            "content": "",
            "choice_id": "",
        }
        return self.handle_ui_response(ui_response)

    def handle_text_input(self, text: str) -> GameResponse:
        ui_response: UiResponse = {
            "msg_id": "ui-text-input",
            "msg_type": UiMsgType.TEXT,
            "content": text,
            "choice_id": "",
        }
        return self.handle_ui_response(ui_response)

    def handle_choice(self, choice_id: str) -> GameResponse:
        ui_response: UiResponse = {
            "msg_id": "ui-choice-input",
            "msg_type": UiMsgType.CHOICE,
            "content": "",
            "choice_id": choice_id,
        }
        return self.handle_ui_response(ui_response)

    def handle_ui_response(self, ui_response: UiResponse) -> GameResponse:
        if self.state == State.FINISHED:
            return self._make_end_response(ui_response["msg_id"])

        if ui_response["msg_type"] == UiMsgType.START:
            response = self.current_scene.start()
            self.state = State.CHARACTER_CREATION
            return self._prepare_response(response, ui_response["msg_id"])

        if ui_response["msg_type"] == UiMsgType.TEXT:
            response = self.current_scene.handle_text_input(ui_response["content"])
            return self._save_scene_progress(response, ui_response["msg_id"])

        if ui_response["msg_type"] == UiMsgType.CHOICE:
            response = self.current_scene.handle_choice(ui_response["choice_id"])
            return self._save_scene_progress(response, ui_response["msg_id"])

        response = make_response(
            "Diese Anfrage kann das Spiel nicht verarbeiten.",
            input_mode=InputMode.NONE,
            character=self.player.get_character_data(),
            title="Fehler",
            msg_type=GameMsgType.ERROR,
        )
        return self._prepare_response(response, ui_response["msg_id"])

    def _save_scene_progress(self, response: GameResponse, answer_id: str) -> GameResponse:
        if self.current_scene is None:
            return self._prepare_response(response, answer_id)

        if self.current_scene.is_done():
            self.player = self.current_scene.get_player()
            self.state = State.SCENE_COMPLETE
            return self._start_next_scene(answer_id, response)

        return self._prepare_response(response, answer_id)

    def _start_next_scene(self, answer_id: str, previous_response: GameResponse) -> GameResponse:
        self.current_scene_id += 1
        next_scene = self._load_scene(self.current_scene_id)
        if next_scene is None:
            self.state = State.FINISHED
            end_response = make_response(
                previous_response["text"],
                input_mode=InputMode.NONE,
                character=self.player.get_character_data(),
                title=previous_response["title"],
                msg_type=GameMsgType.END,
                msg_id="game-end",
            )
            return self._prepare_response(end_response, answer_id)

        self.current_scene = next_scene
        next_response = self.current_scene.start()
        next_response["text"] = previous_response["text"] + "\n\n" + next_response["text"]
        return self._prepare_response(next_response, answer_id)

    def _load_scene(self, scene_id: int) -> Scene | None:
        match scene_id:
            case 0:
                return CharacterCreationScene(scene_id, self.player)
            case 1:
                return BallroomArrivalScene(scene_id, self.player, self.story_flags)

        return None

    def _prepare_response(self, response: GameResponse, answer_id: str) -> GameResponse:
        response["answer_id"] = answer_id
        if response["msg_id"] == "":
            response["msg_id"] = f"game-{self.current_scene_id}-{response['msg_type'].value}"
        return response

    def _make_end_response(self, answer_id: str) -> GameResponse:
        response = make_response(
            "Der aktuelle Spielabschnitt ist abgeschlossen.",
            input_mode=InputMode.NONE,
            character=self.player.get_character_data(),
            title="Ende",
            msg_type=GameMsgType.END,
            msg_id="game-end",
        )
        return self._prepare_response(response, answer_id)
