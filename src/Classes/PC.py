from src.Datatypes.Enums import Attributes, Class, Species
from src.Datatypes.Models import CharacterData


class PC:
    def __init__(
        self,
        name: str = "",
        title: str = "Baron",
        species: Species = Species.NOTSET,
        player_class: Class = Class.NOTSET,
        attributes: dict[Attributes, int] | None = None,
    ) -> None:
        self.name = name
        self.title = title
        self.species = species
        self.player_class = player_class
        self.attributes = attributes or {}

    def get_character_data(self) -> CharacterData:
        data: CharacterData = {
            "name": self.name,
            "title": self.title,
            "species": self.species.get_label() if self.species is not Species.NOTSET else "-",
            "player_class": self.player_class.get_label() if self.player_class is not Class.NOTSET else "-",
            "knowledge": self.attributes[Attributes.KNOWLEDGE],
            "wit": self.attributes[Attributes.WIT],
            "understanding": self.attributes[Attributes.UNDERSTANDING],
            "goal": "-",
        }
        return data