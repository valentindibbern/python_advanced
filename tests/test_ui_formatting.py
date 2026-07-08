import unittest

from src.Classes.Ui import _format_character_line


class UiFormattingTest(unittest.TestCase):
    def test_character_line_wraps_long_values(self) -> None:
        line = _format_character_line(
            "Ziel",
            "Intrigant: Dein Rivale darf am Ende nicht Teil der siegreichen Allianz sein.",
            width=24,
        )

        self.assertIn("\n      ", line)
        self.assertTrue(line.startswith("Ziel: Intrigant: Dein Rivale"))

    def test_character_line_uses_placeholder_for_empty_value(self) -> None:
        self.assertEqual(_format_character_line("Status", ""), "Status: -")


if __name__ == "__main__":
    unittest.main()
