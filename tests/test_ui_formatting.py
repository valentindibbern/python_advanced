import unittest

from src.Classes.Ui import CHARACTER_VALUE_WIDTH, _format_character_line


class UiFormattingTest(unittest.TestCase):
    def test_character_line_wraps_long_values(self) -> None:
        width = 24
        line = _format_character_line(
            "Ziel",
            "Intrigant: Dein Rivale darf am Ende nicht Teil der siegreichen Allianz sein.",
            width=width,
        )
        lines = line.splitlines()

        self.assertGreater(len(lines), 1)
        self.assertTrue(line.startswith("Ziel: Intrigant: Dein Rivale"))
        for wrapped_line in lines[1:]:
            self.assertTrue(wrapped_line.startswith(" " * len("Ziel: ")))
        for wrapped_line in lines:
            self.assertLessEqual(len(wrapped_line), len("Ziel: ") + width)

    def test_status_line_uses_same_indent_for_wrapped_values(self) -> None:
        line = _format_character_line(
            "Status",
            "Verfehlt: Deine Spezies gehört nicht zur siegreichen Allianz.",
            width=18,
        )
        lines = line.splitlines()

        self.assertGreater(len(lines), 1)
        self.assertTrue(lines[0].startswith("Status: Verfehlt:"))
        for wrapped_line in lines[1:]:
            self.assertTrue(wrapped_line.startswith(" " * len("Status: ")))

    def test_character_line_uses_placeholder_for_empty_value(self) -> None:
        self.assertEqual(_format_character_line("Status", ""), "Status: -")

    def test_character_line_does_not_split_long_words(self) -> None:
        line = _format_character_line("Status", "Donaudampfschifffahrtsgesellschaft", width=10)

        self.assertEqual(line, "Status: Donaudampfschifffahrtsgesellschaft")

    def test_default_character_line_width_matches_sidebar(self) -> None:
        line = _format_character_line(
            "Status",
            "Verfehlt: Deine Spezies gehört nicht zur siegreichen Allianz.",
        )

        for wrapped_line in line.splitlines():
            self.assertLessEqual(len(wrapped_line), len("Status: ") + CHARACTER_VALUE_WIDTH)


if __name__ == "__main__":
    unittest.main()
