from __future__ import annotations
from enum import Enum

from src.Utils import make_response, make_choice
from src.Classes.Player import Player
from src.Classes.Scene import Scene
from src.Datatypes.Models import Choice, GameMsgType, GameResponse
from src.Datatypes.Enums import Attributes, Class, Species, InputMode


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


def _get_attribute_choices() -> list[Choice]:
    choices = []

    for main_attribute in Attributes:
        parts = []
        for attribute in Attributes:
            points = 2 if attribute == main_attribute else 1
            parts.append(f"{attribute.get_label()} +{points}")

        choices.append(make_choice(f"attributes:{main_attribute.name}", ", ".join(parts)))

    return choices

def _get_species_choices() -> list[Choice]:
    return [
        {"choice_id": f"species:{species.name}", "label": species.get_label()}
        for species in Species
        if species is not Species.NOTSET
    ]

def _get_class_choices() -> list[Choice]:
    return [
        make_choice(f"class:{player_class.name}", player_class.get_label())
        for player_class in Class
        if player_class is not Class.NOTSET
    ]

def _get_goal_text(player_class: Class, species: Species) -> str:
    if player_class is Class.AUFSTEIGER:
        return (
            "Aufsteiger: Deine Spezies soll Teil der Allianz werden, "
            "die am Ende die Schürfrechte erhält."
        )

    if player_class is Class.INTRIGANT:
        rival = "ein Mensch"
        if species is Species.DWARF:
            rival = "ein Elf"
        elif species is Species.ELF:
            rival = "ein Zwerg"

        return (
            "Intrigant: Dein Rivale darf am Ende nicht Teil der siegreichen "
            f"Allianz sein. Dein Rivale ist {rival}."
        )

    if player_class is Class.NETZWERKER:
        target = "ein Zwerg oder Elf"
        if species in (Species.DWARF, Species.ELF):
            target = "ein Mensch"

        return (
            "Netzwerker: Du willst neue Freundschaften schließen und gewinnen, "
            f"wenn du am Abend eine Person des Königspaars über {target} erreichst."
        )

    return ""


class CharacterCreationScene(Scene):
    def __init__(self, scene_id: int, player: Player) -> None:
        super().__init__(scene_id, player)
        self.step: CharacterCreationStep = CharacterCreationStep.NAME
        self.player: Player = Player()
        self.name: str = ""
        self.player_class: Class = Class.NOTSET
        self.species: Species = Species.NOTSET
        self.attributes: dict[Attributes, int] = {
            Attributes.KNOWLEDGE: 0,
            Attributes.WIT: 0,
            Attributes.UNDERSTANDING: 0,
        }

    def start(self) -> GameResponse:
        self.step = CharacterCreationStep.NAME
        return make_response(
            "Wie heisst dein Charakter?",
            input_mode=InputMode.TEXT,
            character=self.player.get_character_data(),
            title="Charaktererstellung",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-character-name-question",
        )

    def handle_text_input(self, text: str) -> GameResponse:
        text = text.strip()

        if self.step != CharacterCreationStep.NAME:
            return self._response_for_current_step("Bitte wähle eine der angezeigten Optionen.")

        if text == "":
            return make_response(
                "Bitte gib einen Namen ein.",
                input_mode=InputMode.TEXT,
                character=self.player.get_character_data(),
                title="Charaktererstellung",
                msg_type=GameMsgType.ERROR,
                msg_id="game-character-name-error",
            )
        self.name = text
        self.player.name = text
        self.step = CharacterCreationStep.PLAYER_CLASS
        return self._response_for_current_step(
            f"Dein Charakter heißt {self.name}.\n\nWähle eine Klasse."
        )

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

    def get_player(self) -> Player:
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

        if self.player_class is Class.NOTSET:
            return self._response_for_current_step("Bitte wähle eine gültige Klasse.")

        self.player.player_class = self.player_class
        self.step = CharacterCreationStep.SPECIES
        return self._response_for_current_step(
            f"Du hast die Klasse {self.player_class.get_label()} gewählt.\n\nWähle eine Spezies."
        )

    def _handle_species_choice(self, choice_id: str) -> GameResponse:
        prefix = "species:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step("Bitte wähle eine gültige Spezies.")

        species_name = choice_id.removeprefix(prefix)
        try:
            self.species = Species[species_name]
        except KeyError:
            return self._response_for_current_step("Bitte wähle eine gültige Spezies.")

        if self.species is Species.NOTSET:
            return self._response_for_current_step("Bitte wähle eine gültige Spezies.")

        self.player.species = self.species
        self.step = CharacterCreationStep.ATTRIBUTES
        return self._response_for_current_step(
            f"Du hast die Spezies {self.species.get_label()} gewählt.\n\n"
            "Verteile deine 4 Attributpunkte."
        )

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
        self.player.attributes = self.attributes
        self.player.goal = _get_goal_text(self.player_class, self.species)
        self.player.goal_status = "Noch offen"
        self.step = CharacterCreationStep.DONE
        character_summary = (
            f"Name: {self.name}\n"
            f"Klasse: {self.player_class.get_label()}\n"
            f"Spezies: {self.species.get_label()}\n"
            f"Attributwahl: {main_attribute.get_label()}\n"
            f"Ziel: {self.player.goal}"
        )
        return make_response(
            f"Charakter erstellt.\n\n{character_summary}\n\nDu bist bereit für die nächste Szene.",
            input_mode=InputMode.NONE,
            character=self.player.get_character_data(),
            title="Charaktererstellung",
            msg_type=GameMsgType.INFO,
            msg_id="game-character-created",
        )

    def _response_for_current_step(self, text: str) -> GameResponse:
        if self.step == CharacterCreationStep.PLAYER_CLASS:
            return make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=_get_class_choices(),
                character=self.player.get_character_data(),
                title="Charaktererstellung",
                msg_type=GameMsgType.QUESTION,
                msg_id="game-character-class-question",
            )

        if self.step == CharacterCreationStep.SPECIES:
            return make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=_get_species_choices(),
                character=self.player.get_character_data(),
                title="Charaktererstellung",
                msg_type=GameMsgType.QUESTION,
                msg_id="game-character-species-question",
            )

        if self.step == CharacterCreationStep.ATTRIBUTES:
            return make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=_get_attribute_choices(),
                character=self.player.get_character_data(),
                title="Charaktererstellung",
                msg_type=GameMsgType.QUESTION,
                msg_id="game-character-attributes-question",
            )

        return make_response(
            text,
            input_mode=InputMode.TEXT,
            character=self.player.get_character_data(),
            title="Charaktererstellung",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-character-text-question",
        )

    def _get_starting_attributes(self, main_attribute: Attributes) -> dict[Attributes, int]:
        attributes = {
            Attributes.KNOWLEDGE: 0,
            Attributes.WIT: 0,
            Attributes.UNDERSTANDING: 0,
        }

        for attribute in Attributes:
            attributes[attribute] += 2 if attribute == main_attribute else 1

        if self.species is not Species.NOTSET:
            species_bonus = SPECIES_ATTRIBUTE_BONUSES[self.species]
            attributes[species_bonus] += 1

        return attributes
