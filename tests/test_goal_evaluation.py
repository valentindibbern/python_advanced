import unittest

from tests.game_test_helpers import enter_ballroom, play_to_ending, reach_first_talk


class GoalEvaluationTest(unittest.TestCase):
    def test_aufsteiger_human_wins_with_hof(self) -> None:
        _game, response = play_to_ending(
            "class:AUFSTEIGER",
            "species:HUMAN",
            "attributes:WIT",
            "talk:alena",
            "royal:speak",
            "council:hof",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_aufsteiger_human_wins_with_balanced(self) -> None:
        _game, response = play_to_ending(
            "class:AUFSTEIGER",
            "species:HUMAN",
            "attributes:UNDERSTANDING",
            "talk:marik",
            "royal:speak",
            "council:balanced",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_aufsteiger_human_loses_with_gilde(self) -> None:
        _game, response = play_to_ending(
            "class:AUFSTEIGER",
            "species:HUMAN",
            "attributes:KNOWLEDGE",
            "talk:runa",
            "royal:listen",
            "council:gilde",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Verfehlt"))

    def test_aufsteiger_dwarf_wins_with_gilde(self) -> None:
        _game, response = play_to_ending(
            "class:AUFSTEIGER",
            "species:DWARF",
            "attributes:KNOWLEDGE",
            "talk:runa",
            "royal:listen",
            "council:gilde",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_aufsteiger_elf_wins_with_gesandtschaft(self) -> None:
        _game, response = play_to_ending(
            "class:AUFSTEIGER",
            "species:ELF",
            "attributes:UNDERSTANDING",
            "talk:caelion",
            "royal:listen",
            "council:gesandtschaft",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_intrigant_wins_when_rival_is_accused(self) -> None:
        _game, response = play_to_ending(
            "class:INTRIGANT",
            "species:HUMAN",
            "attributes:WIT",
            "talk:alena",
            "royal:accuse",
            "council:hof",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_intrigant_wins_when_rival_alliance_does_not_win(self) -> None:
        _game, response = play_to_ending(
            "class:INTRIGANT",
            "species:DWARF",
            "attributes:KNOWLEDGE",
            "talk:runa",
            "royal:listen",
            "council:gilde",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_intrigant_loses_when_rival_alliance_wins_unblocked(self) -> None:
        _game, response = play_to_ending(
            "class:INTRIGANT",
            "species:HUMAN",
            "attributes:WIT",
            "talk:alena",
            "royal:listen",
            "council:hof",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Verfehlt"))

    def test_netzwerker_wins_with_target_contact_and_royal_contact(self) -> None:
        _game, response = play_to_ending(
            "class:NETZWERKER",
            "species:HUMAN",
            "attributes:WIT",
            "talk:runa",
            "royal:speak",
            "council:gilde",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Erreicht"))

    def test_netzwerker_loses_with_target_contact_but_without_royal_contact(self) -> None:
        _game, response = play_to_ending(
            "class:NETZWERKER",
            "species:HUMAN",
            "attributes:WIT",
            "talk:runa",
            "royal:listen",
            "council:gilde",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Verfehlt"))

    def test_netzwerker_loses_with_royal_contact_but_without_target_contact(self) -> None:
        _game, response = play_to_ending(
            "class:NETZWERKER",
            "species:HUMAN",
            "attributes:WIT",
            "talk:alena",
            "royal:speak",
            "council:hof",
        )

        self.assertTrue(response["character"]["goal_status"].startswith("Verfehlt"))

    def test_talk_updates_intermediate_goal_status(self) -> None:
        game, _response = enter_ballroom(
            "class:NETZWERKER",
            "species:HUMAN",
            "attributes:WIT",
        )
        reach_first_talk(game)

        response = game.handle_choice("talk:runa")

        self.assertIn("Zwischenstand", response["character"]["goal_status"])


if __name__ == "__main__":
    unittest.main()
