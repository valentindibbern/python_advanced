from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from src.Classes.PC import PC
from src.Classes.Scene import Choice
from src.Enums.Attributes import Attributes
from src.Enums.Class import Class
from src.Enums.InputMode import InputMode
from src.Enums.Species import Species

if TYPE_CHECKING:
    from src.Classes.Game import GameResponse


SPECIES_ATTRIBUTE_BONUSES: dict[Species, Attributes] = {
    Species.HUMAN: Attributes.WIT,
    Species.ELF: Attributes.UNDERSTANDING,
    Species.DWARF: Attributes.KNOWLEDGE,
}


class CharacterCreationStep(Enum):
    NAME = 0
    PLAYER_CLASS = 1
    SPECIES = 2
    ATTRIBUTES = 3
    DONE = 4


class CharacterCreationScene:
    def __init__(self) -> None:
        self.scene_id = "0"
        self.step: CharacterCreationStep = CharacterCreationStep.NAME
        self.name: str = ""
        self.player_class: Class | None = None
        self.species: Species | None = None
        self.attributes: dict[Attributes, int] = {}
        self.player: PC | None = None

    def start(self) -> GameResponse:
        self.step = CharacterCreationStep.NAME
        return self._make_response(
            "Charaktererstellung\n\nWie heisst dein Charakter?",
            input_mode=InputMode.TEXT,
        )

    def handle_text_input(self, text: str) -> GameResponse:
        text = text.strip()

        if self.step != CharacterCreationStep.NAME:
            return self._response_for_current_step("Bitte wähle eine der angezeigten Optionen.")

        if text == "":
            return self._make_response(
                "Bitte gib einen Namen ein.",
                input_mode=InputMode.TEXT,
            )

        self.name = text
        self.step = CharacterCreationStep.PLAYER_CLASS
        return self._response_for_current_step("Wähle eine Klasse.")

    def handle_choice(self, choice_id: str) -> GameResponse:
        if self.step == CharacterCreationStep.PLAYER_CLASS:
            return self._handle_class_choice(choice_id)

        if self.step == CharacterCreationStep.SPECIES:
            return self._handle_species_choice(choice_id)

        if self.step == CharacterCreationStep.ATTRIBUTES:
            return self._handle_attribute_choice(choice_id)

        return self._response_for_current_step("Diese Auswahl ist hier nicht möglich.")

    def is_done(self) -> bool:
        return self.step == CharacterCreationStep.DONE

    def get_player(self) -> PC | None:
        return self.player

    def _handle_class_choice(self, choice_id: str) -> GameResponse:
        prefix = "class:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step("Bitte wähle eine gültige Klasse.")

        class_name = choice_id.removeprefix(prefix)
        try:
            self.player_class = Class[class_name]
        except KeyError:
            return self._response_for_current_step("Bitte wähle eine gültige Klasse.")

        self.step = CharacterCreationStep.SPECIES
        return self._response_for_current_step("Wähle eine Spezies.")

    def _handle_species_choice(self, choice_id: str) -> GameResponse:
        prefix = "species:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step("Bitte wähle eine gültige Spezies.")

        species_name = choice_id.removeprefix(prefix)
        try:
            self.species = Species[species_name]
        except KeyError:
            return self._response_for_current_step("Bitte wähle eine gültige Spezies.")

        self.step = CharacterCreationStep.ATTRIBUTES
        return self._response_for_current_step("Verteile deine 4 Attributpunkte.")

    def _handle_attribute_choice(self, choice_id: str) -> GameResponse:
        prefix = "attributes:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step("Bitte wähle eine gültige Attributverteilung.")

        main_attribute_name = choice_id.removeprefix(prefix)
        try:
            main_attribute = Attributes[main_attribute_name]
        except KeyError:
            return self._response_for_current_step("Bitte wähle eine gültige Attributverteilung.")

        self.attributes = self._get_starting_attributes(main_attribute)
        self.player = PC(
            name=self.name,
            species=self.species,
            player_class=self.player_class,
            attributes=self.attributes,
        )
        self.step = CharacterCreationStep.DONE
        return self._make_response(
            "Charakter erstellt.\n\nDu bist bereit für die nächste Szene.",
            input_mode=InputMode.NONE,
            character=self._get_character_data(),
        )

    def _response_for_current_step(self, text: str) -> GameResponse:
        if self.step == CharacterCreationStep.PLAYER_CLASS:
            return self._make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=self._get_class_choices(),
            )

        if self.step == CharacterCreationStep.SPECIES:
            return self._make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=self._get_species_choices(),
            )

        if self.step == CharacterCreationStep.ATTRIBUTES:
            return self._make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=self._get_attribute_choices(),
            )

        return self._make_response(text, input_mode=InputMode.TEXT)

    def _get_class_choices(self) -> list[Choice]:
        return [
            {"id": f"class:{player_class.name}", "label": player_class.get_label()}
            for player_class in Class
        ]

    def _get_species_choices(self) -> list[Choice]:
        return [
            {"id": f"species:{species.name}", "label": species.get_label()}
            for species in Species
        ]

    def _get_attribute_choices(self) -> list[Choice]:
        choices = []

        for main_attribute in Attributes:
            parts = []
            for attribute in Attributes:
                points = 2 if attribute == main_attribute else 1
                parts.append(f"{attribute.get_label()} +{points}")

            choices.append(
                {
                    "id": f"attributes:{main_attribute.name}",
                    "label": ", ".join(parts),
                }
            )

        return choices

    def _get_starting_attributes(self, main_attribute: Attributes) -> dict[Attributes, int]:
        attributes = {
            Attributes.KNOWLEDGE: 0,
            Attributes.WIT: 0,
            Attributes.UNDERSTANDING: 0,
        }

        for attribute in Attributes:
            attributes[attribute] += 2 if attribute == main_attribute else 1

        if self.species is not None:
            species_bonus = SPECIES_ATTRIBUTE_BONUSES[self.species]
            attributes[species_bonus] += 1

        return attributes

    def _get_character_data(self) -> dict[str, str | int] | None:
        if self.player is None:
            return None

        return {
            "name": self.player.name,
            "species": self.player.species.get_label() if self.player.species is not None else "-",
            "player_class": self.player.player_class.get_label()
            if self.player.player_class is not None
            else "-",
            "knowledge": self.player.attributes.get(Attributes.KNOWLEDGE, 0),
            "wit": self.player.attributes.get(Attributes.WIT, 0),
            "understanding": self.player.attributes.get(Attributes.UNDERSTANDING, 0),
            "goal": "-",
        }

    def _make_response(
        self,
        text: str,
        input_mode: InputMode = InputMode.NONE,
        choices: list[Choice] | None = None,
        character: dict[str, str | int] | None = None,
        is_finished: bool = False,
    ) -> GameResponse:
        return {
            "text": text,
            "input_mode": input_mode,
            "choices": choices or [],
            "character": character,
            "is_finished": is_finished,
        }
