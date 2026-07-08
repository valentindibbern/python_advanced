from enum import Enum


class Attributes(Enum):
    KNOWLEDGE = 0
    WIT = 1
    UNDERSTANDING = 2

    def get_label(self) -> str:
        labels = {
            Attributes.KNOWLEDGE: "Wissen",
            Attributes.WIT: "Schlagfertigkeit",
            Attributes.UNDERSTANDING: "Verständnis",
        }
        return labels[self]

class Class(Enum):
    AUFSTEIGER = 0
    INTRIGANT = 1
    NETZWERKER = 2
    NOTSET = 3

    def get_label(self) -> str:
        labels = {
            Class.AUFSTEIGER: "Aufsteiger",
            Class.INTRIGANT: "Intrigant",
            Class.NETZWERKER: "Netzwerker",
            Class.NOTSET: "Nicht gesetzt"
        }
        return labels[self]

class InputMode(Enum):
    TEXT = "text"
    CHOICE = "choice"
    NONE = "none"

class Species(Enum):
    HUMAN = 0
    ELF = 1
    DWARF = 2
    NOTSET = 3

    def get_label(self) -> str:
        labels = {
            Species.HUMAN: "Mensch",
            Species.ELF: "Elf",
            Species.DWARF: "Zwerg",
            Species.NOTSET: "Nicht gesetzt"
        }
        return labels[self]

class State(Enum):
    START = 0
    CHARACTER_CREATION = 1
    FINISHED = 2

