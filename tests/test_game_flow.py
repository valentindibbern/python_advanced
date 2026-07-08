import unittest

from src.Classes.Game import Game
from src.Datatypes.Enums import InputMode, State
from src.Datatypes.Models import GameMsgType
from tests.game_test_helpers import play_to_ending


class GameFlowTest(unittest.TestCase):
    def test_start_shows_start_screen(self) -> None:
        game = Game()

        response = game.start()

        self.assertEqual(response["msg_id"], "game-start-screen")
        self.assertEqual(response["input_mode"], InputMode.NONE)

    def test_full_game_reaches_end_and_stays_finished(self) -> None:
        game, response = play_to_ending(
            "class:AUFSTEIGER",
            "species:HUMAN",
            "attributes:WIT",
            "talk:alena",
            "royal:speak",
            "council:hof",
        )

        self.assertEqual(response["msg_type"], GameMsgType.END)
        self.assertEqual(response["input_mode"], InputMode.NONE)
        self.assertEqual(game.state, State.FINISHED)

        text_response = game.handle_text_input("weiter")
        choice_response = game.handle_choice("continue:ending")

        self.assertEqual(text_response["msg_type"], GameMsgType.END)
        self.assertEqual(choice_response["msg_type"], GameMsgType.END)
        self.assertEqual(text_response["input_mode"], InputMode.NONE)
        self.assertEqual(choice_response["input_mode"], InputMode.NONE)

    def test_invalid_choice_does_not_crash(self) -> None:
        game = Game()
        game.start_game()
        game.handle_text_input("Mira")

        response = game.handle_choice("falsch")

        self.assertEqual(response["msg_type"], GameMsgType.QUESTION)
        self.assertEqual(response["input_mode"], InputMode.CHOICE)

    def test_all_scene_modules_import_with_valid_texts(self) -> None:
        import src.Scenes.scene0.scene
        import src.Scenes.scene1.scene
        import src.Scenes.scene2.scene

        self.assertTrue(src.Scenes.scene0.scene.SYSTEM_TEXTS)
        self.assertTrue(src.Scenes.scene1.scene.SYSTEM_TEXTS)
        self.assertTrue(src.Scenes.scene2.scene.SYSTEM_TEXTS)


if __name__ == "__main__":
    unittest.main()
