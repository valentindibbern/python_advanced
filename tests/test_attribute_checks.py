import unittest
from unittest.mock import patch

from src.Classes.Player import Player
from src.Datatypes.Enums import Attributes
from src.Utils import format_attribute_check, make_attribute_check


class AttributeCheckTest(unittest.TestCase):
    def test_attribute_check_adds_roll_and_attribute_value(self) -> None:
        player = Player(attributes={
            Attributes.KNOWLEDGE: 2,
            Attributes.WIT: 1,
            Attributes.UNDERSTANDING: 1,
        })

        with patch("src.Utils.roll_d6", return_value=4):
            check = make_attribute_check(player, Attributes.KNOWLEDGE, 5)

        self.assertEqual(check["roll"], 4)
        self.assertEqual(check["attribute_value"], 2)
        self.assertEqual(check["total"], 6)
        self.assertTrue(check["success"])

    def test_attribute_check_fails_below_difficulty(self) -> None:
        player = Player(attributes={
            Attributes.KNOWLEDGE: 1,
            Attributes.WIT: 1,
            Attributes.UNDERSTANDING: 1,
        })

        with patch("src.Utils.roll_d6", return_value=2):
            check = make_attribute_check(player, Attributes.UNDERSTANDING, 5)

        self.assertEqual(check["total"], 3)
        self.assertFalse(check["success"])

    def test_format_attribute_check_shows_result(self) -> None:
        player = Player(attributes={
            Attributes.KNOWLEDGE: 1,
            Attributes.WIT: 3,
            Attributes.UNDERSTANDING: 1,
        })

        with patch("src.Utils.roll_d6", return_value=3):
            check = make_attribute_check(player, Attributes.WIT, 6)

        text = format_attribute_check(check)

        self.assertIn("Probe auf Schlagfertigkeit", text)
        self.assertIn("W6 3 + Schlagfertigkeit 3 = 6", text)
        self.assertIn("Erfolg", text)


if __name__ == "__main__":
    unittest.main()
