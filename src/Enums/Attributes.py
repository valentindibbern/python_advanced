from enum import Enum


class Attributes(Enum):
    KNOWLEDGE = 0
    WIT = 1
    UNDERSTANDING = 2

    def get_label(self) -> str:
        labels = {
            Attributes.KNOWLEDGE: "Wissen",
            Attributes.WIT: "Schlagfertigkeit",
            Attributes.UNDERSTANDING: "Verstaendnis",
        }
        return labels[self]
