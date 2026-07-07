from src.Datatypes.Enums import Attributes, Class, Species
from src.Datatypes.Models import PlayerData


class Player:
    def __init__(
        self,
        name: str = "",
        title: str = "Baron",
        species: Species = Species.NOTSET,
        player_class: Class = Class.NOTSET,
        attributes: dict[Attributes, int] | None = None,
        goal: str = ""
    ) -> None:
        self.name = name
        self.title = title
        self.species = species
        self.player_class = player_class
        self.attributes = attributes or {Attributes.KNOWLEDGE: 0, Attributes.WIT: 0, Attributes.UNDERSTANDING: 0}
        self.goal = goal

    def get_character_data(self) -> PlayerData:
        return {
            "name": self.name,
            "title": self.title,
            "species": self.species.get_label() if self.species is not Species.NOTSET else "-",
            "player_class": self.player_class.get_label() if self.player_class is not Class.NOTSET else "-",
            "knowledge": self.attributes[Attributes.KNOWLEDGE],
            "wit": self.attributes[Attributes.WIT],
            "understanding": self.attributes[Attributes.UNDERSTANDING],
            "goal": self.goal,
        }