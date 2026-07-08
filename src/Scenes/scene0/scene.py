from pathlib import Path

from src.Utils import make_response
from src.Utils import get_text, load_text_blocks, require_text_keys
from src.Classes.Player import Player
from src.Classes.Scene import Scene
from src.Datatypes.Enums import InputMode
from src.Datatypes.Models import GameMsgType, GameResponse


TEXT_SOURCE = "scene0/system.txt"
TEXT_DIR = Path(__file__).parent / "texts"
SYSTEM_TEXTS = load_text_blocks(TEXT_DIR / "system.txt")
require_text_keys(SYSTEM_TEXTS, ["start"], TEXT_SOURCE)


class StartScene(Scene):
    def __init__(self, scene_id: int, player: Player) -> None:
        super().__init__(scene_id, player)

    def start(self) -> GameResponse:
        return make_response(
            get_text(SYSTEM_TEXTS, "start", TEXT_SOURCE),
            input_mode=InputMode.NONE,
            character=self.player.get_character_data(),
            title="Start",
            msg_type=GameMsgType.INFO,
            msg_id="game-start-screen",
        )

    def handle_text_input(self, text: str) -> GameResponse:
        return self.start()

    def handle_choice(self, choice_id: str) -> GameResponse:
        return self.start()

    def is_done(self) -> bool:
        return False

    def get_player(self) -> Player:
        return self.player
