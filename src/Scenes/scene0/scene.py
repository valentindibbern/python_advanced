from src.Utils import make_response
from src.Classes.Player import Player
from src.Classes.Scene import Scene
from src.Datatypes.Enums import InputMode
from src.Datatypes.Models import GameMsgType, GameResponse


class StartScene(Scene):
    def __init__(self, scene_id: int, player: Player) -> None:
        super().__init__(scene_id, player)

    def start(self) -> GameResponse:
        return make_response(
            "Vor den Fenstern des Königshofs liegt Schnee. Im Saal dahinter "
            "brennen hundert Kerzen, doch niemand ist nur wegen Musik und Tanz "
            "gekommen.\n\n"
            "Im Nordgrat wurde eine Kristallhöhle entdeckt. Wer heute Abend die "
            "Schürfrechte erhält, gewinnt Einfluss, Geld und vielleicht eine "
            "Schuld, die noch niemand bezahlen will.\n\n"
            "Drücke unten rechts auf Start, um deine Figur zu erstellen. Mit "
            "Stop kannst du das Spiel jederzeit schließen.",
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
