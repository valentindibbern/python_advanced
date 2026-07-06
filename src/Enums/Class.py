from enum import Enum


class Class(Enum):
    AUFSTEIGER = 0
    INTRIGANT = 1
    NETZWERKER = 2

    def get_label(self) -> str:
        labels = {
            Class.AUFSTEIGER: "Aufsteiger",
            Class.INTRIGANT: "Intrigant",
            Class.NETZWERKER: "Netzwerker",
        }
        return labels[self]
