import unittest

from src.Datatypes.Enums import InputMode
from src.Datatypes.Models import GameMsgType
from tests.game_test_helpers import choice_ids, enter_ballroom, reach_first_talk


class BallroomSceneTest(unittest.TestCase):
    def test_arrival_allows_only_look_around(self) -> None:
        _game, response = enter_ballroom()

        self.assertEqual(choice_ids(response), ["continue:look_around"])

    def test_invalid_arrival_choice_stays_in_arrival(self) -> None:
        game, _response = enter_ballroom()

        response = game.handle_choice("continue:first_talk")

        self.assertEqual(response["msg_type"], GameMsgType.QUESTION)
        self.assertEqual(choice_ids(response), ["continue:look_around"])

    def test_observation_requires_three_different_observations(self) -> None:
        game, _response = enter_ballroom()
        response = game.handle_choice("continue:look_around")

        self.assertNotIn("continue:first_talk", choice_ids(response))

        response = game.handle_choice("continue:first_talk")
        self.assertEqual(response["input_mode"], InputMode.CHOICE)
        self.assertNotIn("continue:first_talk", choice_ids(response))

        game.handle_choice("observe:alena")
        game.handle_choice("observe:bastian")
        response = game.handle_choice("observe:runa")

        self.assertIn("continue:first_talk", choice_ids(response))

    def test_duplicate_observation_is_rejected(self) -> None:
        game, _response = enter_ballroom()
        game.handle_choice("continue:look_around")
        game.handle_choice("observe:alena")

        response = game.handle_choice("observe:alena")

        self.assertEqual(response["msg_type"], GameMsgType.QUESTION)
        self.assertIn("observe:bastian", choice_ids(response))

    def test_first_observation_is_saved_in_story_flags(self) -> None:
        game, _response = enter_ballroom()
        game.handle_choice("continue:look_around")

        game.handle_choice("observe:runa")

        self.assertEqual(game.story_flags["first_observed_npc"], "runa")

    def test_first_talk_offers_all_talk_choices(self) -> None:
        game, _response = enter_ballroom()

        response = reach_first_talk(game)

        self.assertEqual(
            choice_ids(response),
            ["talk:alena", "talk:bastian", "talk:runa", "talk:caelion", "talk:marik"],
        )

    def test_invalid_talk_royal_and_council_choices_stay_in_phase(self) -> None:
        game, _response = enter_ballroom()
        reach_first_talk(game)

        talk_response = game.handle_choice("talk:unknown")
        self.assertEqual(choice_ids(talk_response)[0], "talk:alena")

        game.handle_choice("talk:alena")
        royal_response = game.handle_choice("royal:wrong")
        self.assertEqual(choice_ids(royal_response), ["royal:speak", "royal:listen", "royal:accuse"])

        game.handle_choice("royal:speak")
        council_response = game.handle_choice("council:wrong")
        self.assertEqual(
            choice_ids(council_response),
            ["council:hof", "council:gilde", "council:gesandtschaft", "council:balanced"],
        )

    def test_valid_council_choice_opens_ending_choice(self) -> None:
        game, _response = enter_ballroom()
        reach_first_talk(game)
        game.handle_choice("talk:alena")
        game.handle_choice("royal:speak")

        response = game.handle_choice("council:hof")

        self.assertEqual(choice_ids(response), ["continue:ending"])

    def test_final_choice_ends_scene(self) -> None:
        game, _response = enter_ballroom()
        reach_first_talk(game)
        game.handle_choice("talk:alena")
        game.handle_choice("royal:speak")
        game.handle_choice("council:hof")

        response = game.handle_choice("continue:ending")

        self.assertEqual(response["msg_type"], GameMsgType.END)
        self.assertEqual(response["input_mode"], InputMode.NONE)


if __name__ == "__main__":
    unittest.main()
