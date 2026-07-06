from enum import Enum


class Species(Enum):
    HUMAN = 0
    ELF = 1
    DWARF = 2

    def get_label(self) -> str:
        labels = {
            Species.HUMAN: "Mensch",
            Species.ELF: "Elf",
            Species.DWARF: "Zwerg",
        }
        return labels[self]
