import unittest

from src.Datatypes.Enums import InputMode
from src.Datatypes.Models import GameMsgType
from tests.game_test_helpers import choice_ids, create_character
from src.Classes.Game import Game


class CharacterCreationTest(unittest.TestCase):
    def test_start_game_asks_for_name(self) -> None:
        game = Game()

        response = game.start_game()

        self.assertEqual(response["input_mode"], InputMode.TEXT)
        self.assertEqual(response["msg_type"], GameMsgType.QUESTION)

    def test_empty_name_stays_in_name_input(self) -> None:
        game = Game()
        game.start_game()

        response = game.handle_text_input("   ")

        self.assertEqual(response["input_mode"], InputMode.TEXT)
        self.assertEqual(response["msg_type"], GameMsgType.ERROR)
        self.assertEqual(response["character"]["name"], "")

    def test_valid_name_is_trimmed_and_opens_class_choices(self) -> None:
        game = Game()
        game.start_game()

        response = game.handle_text_input("  Mira  ")

        self.assertEqual(response["character"]["name"], "Mira")
        self.assertEqual(
            choice_ids(response),
            ["class:AUFSTEIGER", "class:INTRIGANT", "class:NETZWERKER"],
        )

    def test_invalid_class_stays_in_class_choices(self) -> None:
        game = Game()
        game.start_game()
        game.handle_text_input("Mira")

        response = game.handle_choice("class:FEHLT")

        self.assertEqual(response["input_mode"], InputMode.CHOICE)
        self.assertEqual(
            choice_ids(response),
            ["class:AUFSTEIGER", "class:INTRIGANT", "class:NETZWERKER"],
        )

    def test_valid_class_opens_species_choices(self) -> None:
        game = Game()
        game.start_game()
        game.handle_text_input("Mira")

        response = game.handle_choice("class:INTRIGANT")

        self.assertEqual(response["character"]["player_class"], "Intrigant")
        self.assertEqual(choice_ids(response), ["species:HUMAN", "species:ELF", "species:DWARF"])

    def test_invalid_species_stays_in_species_choices(self) -> None:
        game = Game()
        game.start_game()
        game.handle_text_input("Mira")
        game.handle_choice("class:INTRIGANT")

        response = game.handle_choice("species:ORK")

        self.assertEqual(response["input_mode"], InputMode.CHOICE)
        self.assertEqual(choice_ids(response), ["species:HUMAN", "species:ELF", "species:DWARF"])

    def test_valid_species_opens_attribute_choices(self) -> None:
        game = Game()
        game.start_game()
        game.handle_text_input("Mira")
        game.handle_choice("class:INTRIGANT")

        response = game.handle_choice("species:ELF")

        self.assertEqual(response["character"]["species"], "Elf")
        self.assertEqual(
            choice_ids(response),
            ["attributes:KNOWLEDGE", "attributes:WIT", "attributes:UNDERSTANDING"],
        )

    def test_invalid_attribute_stays_in_attribute_choices(self) -> None:
        game = Game()
        game.start_game()
        game.handle_text_input("Mira")
        game.handle_choice("class:INTRIGANT")
        game.handle_choice("species:ELF")

        response = game.handle_choice("attributes:LUCK")

        self.assertEqual(response["input_mode"], InputMode.CHOICE)
        self.assertEqual(
            choice_ids(response),
            ["attributes:KNOWLEDGE", "attributes:WIT", "attributes:UNDERSTANDING"],
        )

    def test_valid_attribute_finishes_character_and_starts_ballroom(self) -> None:
        _game, response = create_character("class:NETZWERKER", "species:DWARF", "attributes:KNOWLEDGE")

        self.assertEqual(response["msg_id"], "game-ballroom-arrival")
        self.assertEqual(response["input_mode"], InputMode.CHOICE)
        self.assertEqual(response["character"]["name"], "Testname")
        self.assertEqual(response["character"]["player_class"], "Netzwerker")
        self.assertEqual(response["character"]["species"], "Zwerg")
        self.assertEqual(response["character"]["goal_status"], "Noch offen")


if __name__ == "__main__":
    unittest.main()
