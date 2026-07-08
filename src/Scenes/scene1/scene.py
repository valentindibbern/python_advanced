from __future__ import annotations
from enum import Enum
from pathlib import Path

from src.Utils import (
    format_text,
    get_text,
    load_text_blocks,
    make_choice,
    make_response,
    require_text_keys,
)
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


TEXT_DIR = Path(__file__).parent / "texts"
SYSTEM_TEXT_SOURCE = "scene1/system.txt"
SYSTEM_TEXTS = load_text_blocks(TEXT_DIR / "system.txt")

CLASS_TEXT_SOURCES: dict[Class, str] = {
    Class.AUFSTEIGER: "scene1/class_aufsteiger.txt",
    Class.INTRIGANT: "scene1/class_intrigant.txt",
    Class.NETZWERKER: "scene1/class_netzwerker.txt",
}
CLASS_TEXTS: dict[Class, dict[str, str]] = {
    Class.AUFSTEIGER: load_text_blocks(TEXT_DIR / "class_aufsteiger.txt"),
    Class.INTRIGANT: load_text_blocks(TEXT_DIR / "class_intrigant.txt"),
    Class.NETZWERKER: load_text_blocks(TEXT_DIR / "class_netzwerker.txt"),
}

SPECIES_TEXT_SOURCES: dict[Species, str] = {
    Species.HUMAN: "scene1/species_human.txt",
    Species.ELF: "scene1/species_elf.txt",
    Species.DWARF: "scene1/species_dwarf.txt",
}
SPECIES_TEXTS: dict[Species, dict[str, str]] = {
    Species.HUMAN: load_text_blocks(TEXT_DIR / "species_human.txt"),
    Species.ELF: load_text_blocks(TEXT_DIR / "species_elf.txt"),
    Species.DWARF: load_text_blocks(TEXT_DIR / "species_dwarf.txt"),
}

require_text_keys(
    SYSTEM_TEXTS,
    [
        "name_question",
        "name_empty_error",
        "wrong_input_mode",
        "name_saved",
        "invalid_choice",
        "invalid_class",
        "class_selected",
        "invalid_species",
        "species_selected",
        "invalid_attributes",
        "attribute_intro",
        "attribute_choice_knowledge",
        "attribute_choice_wit",
        "attribute_choice_understanding",
        "character_created",
        "goal_aufsteiger",
        "goal_intrigant",
        "goal_netzwerker",
    ],
    SYSTEM_TEXT_SOURCE,
)
for player_class, texts in CLASS_TEXTS.items():
    require_text_keys(texts, ["choice_label", "story"], CLASS_TEXT_SOURCES[player_class])
for species, texts in SPECIES_TEXTS.items():
    require_text_keys(texts, ["choice_label", "story"], SPECIES_TEXT_SOURCES[species])


def _get_attribute_choices() -> list[Choice]:
    labels = {
        Attributes.KNOWLEDGE: get_text(
            SYSTEM_TEXTS, "attribute_choice_knowledge", SYSTEM_TEXT_SOURCE
        ),
        Attributes.WIT: get_text(SYSTEM_TEXTS, "attribute_choice_wit", SYSTEM_TEXT_SOURCE),
        Attributes.UNDERSTANDING: get_text(
            SYSTEM_TEXTS, "attribute_choice_understanding", SYSTEM_TEXT_SOURCE
        ),
    }
    return [make_choice(f"attributes:{attribute.name}", labels[attribute]) for attribute in Attributes]


def _get_species_choices() -> list[Choice]:
    return [
        make_choice(
            f"species:{species.name}",
            get_text(SPECIES_TEXTS[species], "choice_label", SPECIES_TEXT_SOURCES[species]),
        )
        for species in Species
        if species is not Species.NOTSET
    ]


def _get_class_choices() -> list[Choice]:
    return [
        make_choice(
            f"class:{player_class.name}",
            get_text(CLASS_TEXTS[player_class], "choice_label", CLASS_TEXT_SOURCES[player_class]),
        )
        for player_class in Class
        if player_class is not Class.NOTSET
    ]


def _class_story_text(player_class: Class) -> str:
    return get_text(CLASS_TEXTS[player_class], "story", CLASS_TEXT_SOURCES[player_class])


def _species_story_text(species: Species) -> str:
    return get_text(SPECIES_TEXTS[species], "story", SPECIES_TEXT_SOURCES[species])


def _attribute_intro_text() -> str:
    return get_text(SYSTEM_TEXTS, "attribute_intro", SYSTEM_TEXT_SOURCE)


def _get_goal_text(player_class: Class, species: Species) -> str:
    if player_class is Class.AUFSTEIGER:
        return get_text(SYSTEM_TEXTS, "goal_aufsteiger", SYSTEM_TEXT_SOURCE)

    if player_class is Class.INTRIGANT:
        rival = "ein Mensch"
        if species is Species.DWARF:
            rival = "ein Elf"
        elif species is Species.ELF:
            rival = "ein Zwerg"

        return format_text(SYSTEM_TEXTS, "goal_intrigant", SYSTEM_TEXT_SOURCE, rival=rival)

    if player_class is Class.NETZWERKER:
        target = "ein Zwerg oder Elf"
        if species in (Species.DWARF, Species.ELF):
            target = "ein Mensch"

        return format_text(SYSTEM_TEXTS, "goal_netzwerker", SYSTEM_TEXT_SOURCE, target=target)

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
            get_text(SYSTEM_TEXTS, "name_question", SYSTEM_TEXT_SOURCE),
            input_mode=InputMode.TEXT,
            character=self.player.get_character_data(),
            title="Charaktererstellung",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-character-name-question",
        )

    def handle_text_input(self, text: str) -> GameResponse:
        text = text.strip()

        if self.step != CharacterCreationStep.NAME:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "wrong_input_mode", SYSTEM_TEXT_SOURCE)
            )

        if text == "":
            return make_response(
                get_text(SYSTEM_TEXTS, "name_empty_error", SYSTEM_TEXT_SOURCE),
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
            format_text(SYSTEM_TEXTS, "name_saved", SYSTEM_TEXT_SOURCE, name=self.name)
        )

    def handle_choice(self, choice_id: str) -> GameResponse:
        if self.step == CharacterCreationStep.PLAYER_CLASS:
            return self._handle_class_choice(choice_id)

        if self.step == CharacterCreationStep.SPECIES:
            return self._handle_species_choice(choice_id)

        if self.step == CharacterCreationStep.ATTRIBUTES:
            return self._handle_attribute_choice(choice_id)

        return self._response_for_current_step(get_text(SYSTEM_TEXTS, "invalid_choice", SYSTEM_TEXT_SOURCE))

    def is_done(self) -> bool:
        return self.step == CharacterCreationStep.DONE

    def get_player(self) -> Player:
        return self.player

    def _handle_class_choice(self, choice_id: str) -> GameResponse:
        prefix = "class:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_class", SYSTEM_TEXT_SOURCE)
            )

        class_name = choice_id.removeprefix(prefix)
        try:
            self.player_class = Class[class_name]
        except KeyError:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_class", SYSTEM_TEXT_SOURCE)
            )

        if self.player_class is Class.NOTSET:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_class", SYSTEM_TEXT_SOURCE)
            )

        self.player.player_class = self.player_class
        self.step = CharacterCreationStep.SPECIES
        return self._response_for_current_step(
            format_text(
                SYSTEM_TEXTS,
                "class_selected",
                SYSTEM_TEXT_SOURCE,
                player_class=self.player_class.get_label(),
                class_story=_class_story_text(self.player_class),
            )
        )

    def _handle_species_choice(self, choice_id: str) -> GameResponse:
        prefix = "species:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_species", SYSTEM_TEXT_SOURCE)
            )

        species_name = choice_id.removeprefix(prefix)
        try:
            self.species = Species[species_name]
        except KeyError:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_species", SYSTEM_TEXT_SOURCE)
            )

        if self.species is Species.NOTSET:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_species", SYSTEM_TEXT_SOURCE)
            )

        self.player.species = self.species
        self.step = CharacterCreationStep.ATTRIBUTES
        return self._response_for_current_step(
            format_text(
                SYSTEM_TEXTS,
                "species_selected",
                SYSTEM_TEXT_SOURCE,
                species=self.species.get_label(),
                species_story=_species_story_text(self.species),
                attribute_intro=_attribute_intro_text(),
            )
        )

    def _handle_attribute_choice(self, choice_id: str) -> GameResponse:
        prefix = "attributes:"
        if not choice_id.startswith(prefix):
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_attributes", SYSTEM_TEXT_SOURCE)
            )

        main_attribute_name = choice_id.removeprefix(prefix)
        try:
            main_attribute = Attributes[main_attribute_name]
        except KeyError:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_attributes", SYSTEM_TEXT_SOURCE)
            )

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
            format_text(
                SYSTEM_TEXTS,
                "character_created",
                SYSTEM_TEXT_SOURCE,
                character_summary=character_summary,
            ),
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
