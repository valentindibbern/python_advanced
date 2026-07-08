import unittest

from tests.game_test_helpers import create_character


class AttributeBonusTest(unittest.TestCase):
    def test_human_adds_wit_bonus(self) -> None:
        _game, response = create_character("class:AUFSTEIGER", "species:HUMAN", "attributes:KNOWLEDGE")

        self.assertEqual(response["character"]["knowledge"], 2)
        self.assertEqual(response["character"]["wit"], 2)
        self.assertEqual(response["character"]["understanding"], 1)

    def test_elf_adds_understanding_bonus(self) -> None:
        _game, response = create_character("class:AUFSTEIGER", "species:ELF", "attributes:KNOWLEDGE")

        self.assertEqual(response["character"]["knowledge"], 2)
        self.assertEqual(response["character"]["wit"], 1)
        self.assertEqual(response["character"]["understanding"], 2)

    def test_dwarf_adds_knowledge_bonus(self) -> None:
        _game, response = create_character("class:AUFSTEIGER", "species:DWARF", "attributes:WIT")

        self.assertEqual(response["character"]["knowledge"], 2)
        self.assertEqual(response["character"]["wit"], 2)
        self.assertEqual(response["character"]["understanding"], 1)

    def test_species_bonus_stacks_with_main_attribute(self) -> None:
        _game, response = create_character("class:AUFSTEIGER", "species:DWARF", "attributes:KNOWLEDGE")

        self.assertEqual(response["character"]["knowledge"], 3)
        self.assertEqual(response["character"]["wit"], 1)
        self.assertEqual(response["character"]["understanding"], 1)


if __name__ == "__main__":
    unittest.main()
