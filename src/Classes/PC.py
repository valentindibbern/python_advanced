from src.Enums.Attributes import Attributes
from src.Enums.Class import Class
from src.Enums.Species import Species


class PC:
    def __init__(
        self,
        name: str = "",
        species: Species | None = None,
        player_class: Class | None = None,
        attributes: dict[Attributes, int] | None = None,
    ) -> None:
        self.name = name
        self.species = species
        self.player_class = player_class
        self.attributes = attributes or {}
