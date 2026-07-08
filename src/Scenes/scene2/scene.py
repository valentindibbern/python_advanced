from __future__ import annotations
from enum import Enum
from pathlib import Path

from src.Utils import (
    format_attribute_check,
    format_text,
    get_text,
    load_text_blocks,
    make_attribute_check,
    make_choice,
    make_response,
    require_text_keys,
)
from src.Classes.Player import Player
from src.Classes.Scene import Scene
from src.Datatypes.Models import Choice, GameMsgType, GameResponse
from src.Datatypes.Enums import Attributes, Class, InputMode, Species


class BallroomStep(Enum):
    ARRIVAL = 0
    OBSERVATION = 1
    FIRST_TALK = 2
    ROYAL_INTERMEZZO = 3
    COUNCIL = 4
    FINAL = 5
    DONE = 6


NPC_NAMES: dict[str, str] = {
    "alena": "Herzogin Alena von Falkenruh",
    "bastian": "Graf Bastian von Eisenmark",
    "runa": "Meisterin Runa Steinhand",
    "caelion": "Lord Caelion Silberblatt",
    "marik": "Hofsekretär Marik Voss",
    "queen": "Königin Meridia",
    "king": "König Arwed",
}

SPECIES_ALLIANCES: dict[Species, str] = {
    Species.HUMAN: "hof",
    Species.DWARF: "gilde",
    Species.ELF: "gesandtschaft",
}

ALLIANCE_LABELS: dict[str, str] = {
    "hof": "königliche Hofallianz",
    "gilde": "Gildenpakt",
    "gesandtschaft": "elfische Gesandtschaft",
    "balanced": "gemeinsamer Kronenpakt",
}

OBSERVATION_CHOICE_IDS: list[str] = [
    "observe:alena",
    "observe:bastian",
    "observe:runa",
    "observe:caelion",
    "observe:marik",
]

TALK_TARGETS: dict[str, tuple[str, str]] = {
    "talk:alena": ("alena", "hof"),
    "talk:bastian": ("bastian", "hof"),
    "talk:runa": ("runa", "gilde"),
    "talk:caelion": ("caelion", "gesandtschaft"),
    "talk:marik": ("marik", "balanced"),
}

NPC_SPECIES: dict[str, Species] = {
    "alena": Species.HUMAN,
    "bastian": Species.HUMAN,
    "runa": Species.DWARF,
    "caelion": Species.ELF,
    "marik": Species.HUMAN,
}

OBSERVATION_CHECKS: dict[str, tuple[Attributes, int, str, str, str]] = {
    "observe:alena": (
        Attributes.UNDERSTANDING,
        5,
        "hint:alena",
        "check_alena_success",
        "check_alena_failure",
    ),
    "observe:bastian": (
        Attributes.WIT,
        5,
        "hint:bastian",
        "check_bastian_success",
        "check_bastian_failure",
    ),
    "observe:runa": (
        Attributes.KNOWLEDGE,
        5,
        "hint:runa",
        "check_runa_success",
        "check_runa_failure",
    ),
    "observe:caelion": (
        Attributes.UNDERSTANDING,
        5,
        "hint:caelion",
        "check_caelion_success",
        "check_caelion_failure",
    ),
    "observe:marik": (
        Attributes.KNOWLEDGE,
        6,
        "hint:marik",
        "check_marik_success",
        "check_marik_failure",
    ),
}

COUNCIL_ALLIANCES: dict[str, str] = {
    "council:hof": "hof",
    "council:gilde": "gilde",
    "council:gesandtschaft": "gesandtschaft",
    "council:balanced": "balanced",
    "council:gilde_safety": "gilde",
    "council:gesandtschaft_rights": "gesandtschaft",
    "council:balanced_documents": "balanced",
}

COUNCIL_ATTRIBUTES: dict[str, Attributes] = {
    "hof": Attributes.WIT,
    "gilde": Attributes.KNOWLEDGE,
    "gesandtschaft": Attributes.UNDERSTANDING,
    "balanced": Attributes.UNDERSTANDING,
}

BONUS_COUNCIL_CHOICES: dict[str, tuple[str, str]] = {
    "hint:runa": ("council:gilde_safety", "choice_council_gilde_safety"),
    "hint:caelion": ("council:gesandtschaft_rights", "choice_council_gesandtschaft_rights"),
    "hint:marik": ("council:balanced_documents", "choice_council_balanced_documents"),
}

TEXT_DIR = Path(__file__).parent / "texts"
SYSTEM_TEXT_SOURCE = "scene2/system.txt"
SYSTEM_TEXTS = load_text_blocks(TEXT_DIR / "system.txt")

NPC_TEXT_SOURCES: dict[str, str] = {
    "alena": "scene2/alena.txt",
    "bastian": "scene2/bastian.txt",
    "runa": "scene2/runa.txt",
    "caelion": "scene2/caelion.txt",
    "marik": "scene2/marik.txt",
    "queen": "scene2/queen.txt",
    "king": "scene2/king.txt",
}
NPC_TEXTS: dict[str, dict[str, str]] = {
    npc_id: load_text_blocks(TEXT_DIR / f"{npc_id}.txt")
    for npc_id in NPC_TEXT_SOURCES
}

require_text_keys(
    SYSTEM_TEXTS,
    [
        "arrival",
        "choice_look_around",
        "done",
        "invalid_choice",
        "overview",
        "first_talk_start",
        "invalid_observation",
        "already_observed",
        "observation_done_hint",
        "invalid_talk",
        "talk_royal_transition",
        "royal_speak",
        "royal_speak_responsibility",
        "royal_accuse",
        "royal_accuse_bastian",
        "royal_listen",
        "council_transition",
        "invalid_council",
        "council_balanced",
        "council_default",
        "council_gilde_safety",
        "council_gesandtschaft_rights",
        "council_balanced_documents",
        "council_check_success",
        "council_check_failure",
        "council_after",
        "choice_ending",
        "ending",
        "status_prefix",
        "status_royal_contact",
        "status_aufsteiger_contact",
        "status_aufsteiger_missing",
        "status_netzwerker_contact",
        "ending_aufsteiger_success",
        "ending_aufsteiger_failure",
        "ending_intrigant_success",
        "ending_intrigant_failure",
        "ending_netzwerker_success",
        "ending_netzwerker_failure",
        "choice_observe_alena",
        "choice_observe_bastian",
        "choice_observe_runa",
        "choice_observe_caelion",
        "choice_observe_marik",
        "choice_first_talk",
        "choice_talk_alena",
        "choice_talk_bastian",
        "choice_talk_runa",
        "choice_talk_caelion",
        "choice_talk_marik",
        "choice_royal_speak",
        "choice_royal_speak_responsibility",
        "choice_royal_listen",
        "choice_royal_accuse",
        "choice_royal_accuse_bastian",
        "choice_council_hof",
        "choice_council_gilde",
        "choice_council_gesandtschaft",
        "choice_council_balanced",
        "choice_council_gilde_safety",
        "choice_council_gesandtschaft_rights",
        "choice_council_balanced_documents",
        "check_alena_success",
        "check_alena_failure",
        "check_bastian_success",
        "check_bastian_failure",
        "check_runa_success",
        "check_runa_failure",
        "check_caelion_success",
        "check_caelion_failure",
        "check_marik_success",
        "check_marik_failure",
    ],
    SYSTEM_TEXT_SOURCE,
)
for npc_id, texts in NPC_TEXTS.items():
    if npc_id in ("queen", "king"):
        require_text_keys(texts, ["note"], NPC_TEXT_SOURCES[npc_id])
    else:
        require_text_keys(texts, ["observe", "memory", "talk"], NPC_TEXT_SOURCES[npc_id])


def _rival_species(player_species: Species) -> Species:
    if player_species is Species.HUMAN:
        return Species.HUMAN
    if player_species is Species.DWARF:
        return Species.ELF
    return Species.DWARF


def _network_target_species(player_species: Species) -> tuple[Species, ...]:
    if player_species is Species.HUMAN:
        return (Species.DWARF, Species.ELF)
    return (Species.HUMAN,)


def _overview_text() -> str:
    return get_text(SYSTEM_TEXTS, "overview", SYSTEM_TEXT_SOURCE)


def _observation_text(choice_id: str) -> str:
    npc_id = choice_id.removeprefix("observe:")
    return get_text(NPC_TEXTS[npc_id], "observe", NPC_TEXT_SOURCES[npc_id])


def _first_observation_memory(npc_id: str) -> str:
    if npc_id not in NPC_TEXTS:
        return ""
    return get_text(NPC_TEXTS[npc_id], "memory", NPC_TEXT_SOURCES[npc_id])


class BallroomArrivalScene(Scene):
    def __init__(self, scene_id: int, player: Player, story_flags: dict[str, str]) -> None:
        super().__init__(scene_id, player)
        self.story_flags = story_flags
        self.step: BallroomStep = BallroomStep.ARRIVAL
        self.observed_choices: list[str] = []
        self.talked_to: str = ""
        self.royal_contact: bool = False
        self.network_contact: bool = False
        self.rival_blocked: bool = False
        self.supported_alliance: str = ""
        self.winning_alliance: str = ""

    def start(self) -> GameResponse:
        self.step = BallroomStep.ARRIVAL
        return make_response(
            format_text(
                SYSTEM_TEXTS,
                "arrival",
                SYSTEM_TEXT_SOURCE,
                title=self.player.title,
                name=self.player.name,
            ),
            input_mode=InputMode.CHOICE,
            choices=[
                make_choice(
                    "continue:look_around",
                    get_text(SYSTEM_TEXTS, "choice_look_around", SYSTEM_TEXT_SOURCE),
                )
            ],
            character=self.player.get_character_data(),
            title="Ankunft im Ballsaal",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-arrival",
        )

    def handle_text_input(self, text: str) -> GameResponse:
        return self._response_for_current_step(get_text(SYSTEM_TEXTS, "invalid_choice", SYSTEM_TEXT_SOURCE))

    def handle_choice(self, choice_id: str) -> GameResponse:
        if self.step is BallroomStep.ARRIVAL:
            return self._handle_arrival(choice_id)
        if self.step is BallroomStep.OBSERVATION:
            return self._handle_observation(choice_id)
        if self.step is BallroomStep.FIRST_TALK:
            return self._handle_talk(choice_id)
        if self.step is BallroomStep.ROYAL_INTERMEZZO:
            return self._handle_royal_intermezzo(choice_id)
        if self.step is BallroomStep.COUNCIL:
            return self._handle_council(choice_id)
        if self.step is BallroomStep.FINAL:
            return self._handle_final(choice_id)

        return make_response(
            get_text(SYSTEM_TEXTS, "done", SYSTEM_TEXT_SOURCE),
            input_mode=InputMode.NONE,
            character=self.player.get_character_data(),
            title="Ende",
            msg_type=GameMsgType.END,
            msg_id="game-ballroom-done",
        )

    def is_done(self) -> bool:
        return self.step is BallroomStep.DONE

    def get_player(self) -> Player:
        return self.player

    def _handle_arrival(self, choice_id: str) -> GameResponse:
        if choice_id != "continue:look_around":
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_choice", SYSTEM_TEXT_SOURCE)
            )

        self.step = BallroomStep.OBSERVATION
        return make_response(
            _overview_text(),
            input_mode=InputMode.CHOICE,
            choices=self._observation_choices(),
            character=self.player.get_character_data(),
            title="Die Gäste",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-overview",
        )

    def _handle_observation(self, choice_id: str) -> GameResponse:
        if choice_id == "continue:first_talk" and len(self.observed_choices) >= 3:
            self.step = BallroomStep.FIRST_TALK
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            return make_response(
                format_text(
                    SYSTEM_TEXTS,
                    "first_talk_start",
                    SYSTEM_TEXT_SOURCE,
                    memory_text=memory_text,
                ),
                input_mode=InputMode.CHOICE,
                choices=self._talk_choices(),
                character=self.player.get_character_data(),
                title="Erstes Gespräch",
                msg_type=GameMsgType.QUESTION,
                msg_id="game-ballroom-first-talk-start",
            )

        if choice_id not in self._observation_choice_ids():
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_observation", SYSTEM_TEXT_SOURCE)
            )

        if choice_id in self.observed_choices:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "already_observed", SYSTEM_TEXT_SOURCE)
            )

        self.observed_choices.append(choice_id)
        text = _observation_text(choice_id)
        check_text = self._run_observation_check(choice_id)
        if check_text != "":
            text += "\n\n" + check_text

        if len(self.observed_choices) == 1:
            self.story_flags["first_observed_npc"] = choice_id.removeprefix("observe:")

        if len(self.observed_choices) >= 3:
            text += "\n\n" + get_text(SYSTEM_TEXTS, "observation_done_hint", SYSTEM_TEXT_SOURCE)

        return make_response(
            text,
            input_mode=InputMode.CHOICE,
            choices=self._observation_choices(),
            character=self.player.get_character_data(),
            title="Beobachtung",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-observation",
        )

    def _handle_talk(self, choice_id: str) -> GameResponse:
        if choice_id not in TALK_TARGETS:
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_talk", SYSTEM_TEXT_SOURCE)
            )

        npc_id, alliance = TALK_TARGETS[choice_id]
        self.talked_to = npc_id
        self.supported_alliance = alliance
        self._update_goal_status_after_talk(npc_id, alliance)
        self.step = BallroomStep.ROYAL_INTERMEZZO
        return make_response(
            self._talk_text(npc_id)
            + "\n\n"
            + get_text(SYSTEM_TEXTS, "talk_royal_transition", SYSTEM_TEXT_SOURCE),
            input_mode=InputMode.CHOICE,
            choices=self._royal_choices(),
            character=self.player.get_character_data(),
            title="Gespräch",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-talk",
        )

    def _handle_royal_intermezzo(self, choice_id: str) -> GameResponse:
        if choice_id not in self._royal_choice_ids():
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_choice", SYSTEM_TEXT_SOURCE)
            )

        if choice_id in ("royal:speak", "royal:speak_responsibility"):
            self.royal_contact = True
            self.player.goal_status = self._status_text(
                get_text(SYSTEM_TEXTS, "status_royal_contact", SYSTEM_TEXT_SOURCE)
            )
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            text_key = "royal_speak_responsibility" if choice_id == "royal:speak_responsibility" else "royal_speak"
            text = format_text(SYSTEM_TEXTS, text_key, SYSTEM_TEXT_SOURCE, memory_text=memory_text)
        elif choice_id in ("royal:accuse", "royal:accuse_bastian"):
            self.rival_blocked = True
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            text_key = "royal_accuse_bastian" if choice_id == "royal:accuse_bastian" else "royal_accuse"
            text = format_text(SYSTEM_TEXTS, text_key, SYSTEM_TEXT_SOURCE, memory_text=memory_text)
        else:
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            text = format_text(SYSTEM_TEXTS, "royal_listen", SYSTEM_TEXT_SOURCE, memory_text=memory_text)

        self.step = BallroomStep.COUNCIL
        return make_response(
            text
            + "\n\n"
            + get_text(SYSTEM_TEXTS, "council_transition", SYSTEM_TEXT_SOURCE),
            input_mode=InputMode.CHOICE,
            choices=self._council_choices(),
            character=self.player.get_character_data(),
            title="Vor dem Königspaar",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-royal",
        )

    def _handle_council(self, choice_id: str) -> GameResponse:
        if choice_id not in self._council_choice_ids():
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_council", SYSTEM_TEXT_SOURCE)
            )

        self.supported_alliance = COUNCIL_ALLIANCES[choice_id]
        self.winning_alliance = self._choose_winning_alliance()
        self._evaluate_goal()
        self.step = BallroomStep.FINAL
        return make_response(
            self._council_text(choice_id)
            + "\n\n"
            + get_text(SYSTEM_TEXTS, "council_after", SYSTEM_TEXT_SOURCE),
            input_mode=InputMode.CHOICE,
            choices=[
                make_choice(
                    "continue:ending",
                    get_text(SYSTEM_TEXTS, "choice_ending", SYSTEM_TEXT_SOURCE),
                )
            ],
            character=self.player.get_character_data(),
            title="Ratssaal",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-council",
        )

    def _handle_final(self, choice_id: str) -> GameResponse:
        if choice_id != "continue:ending":
            return self._response_for_current_step(
                get_text(SYSTEM_TEXTS, "invalid_choice", SYSTEM_TEXT_SOURCE)
            )

        self.step = BallroomStep.DONE
        success = self.player.goal_status.startswith("Erreicht")
        result = self._personal_ending_text(success)
        return make_response(
            format_text(
                SYSTEM_TEXTS,
                "ending",
                SYSTEM_TEXT_SOURCE,
                alliance_label=ALLIANCE_LABELS[self.winning_alliance],
                result=result,
                goal_status=self.player.goal_status,
            ),
            input_mode=InputMode.NONE,
            character=self.player.get_character_data(),
            title="Ende des Ballabends",
            msg_type=GameMsgType.END,
            msg_id="game-ballroom-ending",
        )

    def _response_for_current_step(self, text: str) -> GameResponse:
        if self.step is BallroomStep.OBSERVATION:
            choices = self._observation_choices()
        elif self.step is BallroomStep.FIRST_TALK:
            choices = self._talk_choices()
        elif self.step is BallroomStep.ROYAL_INTERMEZZO:
            choices = self._royal_choices()
        elif self.step is BallroomStep.COUNCIL:
            choices = self._council_choices()
        elif self.step is BallroomStep.FINAL:
            choices = [
                make_choice(
                    "continue:ending",
                    get_text(SYSTEM_TEXTS, "choice_ending", SYSTEM_TEXT_SOURCE),
                )
            ]
        else:
            choices = [
                make_choice(
                    "continue:look_around",
                    get_text(SYSTEM_TEXTS, "choice_look_around", SYSTEM_TEXT_SOURCE),
                )
            ]

        return make_response(
            text,
            input_mode=InputMode.CHOICE,
            choices=choices,
            character=self.player.get_character_data(),
            title="Ballsaal",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-choice-error",
        )

    def _observation_choice_ids(self) -> list[str]:
        return OBSERVATION_CHOICE_IDS

    def _observation_choices(self) -> list[Choice]:
        labels = {
            "observe:alena": get_text(SYSTEM_TEXTS, "choice_observe_alena", SYSTEM_TEXT_SOURCE),
            "observe:bastian": get_text(SYSTEM_TEXTS, "choice_observe_bastian", SYSTEM_TEXT_SOURCE),
            "observe:runa": get_text(SYSTEM_TEXTS, "choice_observe_runa", SYSTEM_TEXT_SOURCE),
            "observe:caelion": get_text(SYSTEM_TEXTS, "choice_observe_caelion", SYSTEM_TEXT_SOURCE),
            "observe:marik": get_text(SYSTEM_TEXTS, "choice_observe_marik", SYSTEM_TEXT_SOURCE),
        }
        choices = [
            make_choice(choice_id, label)
            for choice_id, label in labels.items()
            if choice_id not in self.observed_choices
        ]
        if len(self.observed_choices) >= 3:
            choices.append(
                make_choice(
                    "continue:first_talk",
                    get_text(SYSTEM_TEXTS, "choice_first_talk", SYSTEM_TEXT_SOURCE),
                )
            )
        return choices

    def _talk_choices(self) -> list[Choice]:
        return [
            make_choice("talk:alena", get_text(SYSTEM_TEXTS, "choice_talk_alena", SYSTEM_TEXT_SOURCE)),
            make_choice(
                "talk:bastian",
                get_text(SYSTEM_TEXTS, "choice_talk_bastian", SYSTEM_TEXT_SOURCE),
            ),
            make_choice("talk:runa", get_text(SYSTEM_TEXTS, "choice_talk_runa", SYSTEM_TEXT_SOURCE)),
            make_choice(
                "talk:caelion",
                get_text(SYSTEM_TEXTS, "choice_talk_caelion", SYSTEM_TEXT_SOURCE),
            ),
            make_choice("talk:marik", get_text(SYSTEM_TEXTS, "choice_talk_marik", SYSTEM_TEXT_SOURCE)),
        ]

    def _royal_choices(self) -> list[Choice]:
        choices = [
            make_choice("royal:speak", get_text(SYSTEM_TEXTS, "choice_royal_speak", SYSTEM_TEXT_SOURCE)),
            make_choice("royal:listen", get_text(SYSTEM_TEXTS, "choice_royal_listen", SYSTEM_TEXT_SOURCE)),
            make_choice("royal:accuse", get_text(SYSTEM_TEXTS, "choice_royal_accuse", SYSTEM_TEXT_SOURCE)),
        ]
        if self.story_flags.get("hint:alena") == "success":
            choices.append(
                make_choice(
                    "royal:speak_responsibility",
                    get_text(SYSTEM_TEXTS, "choice_royal_speak_responsibility", SYSTEM_TEXT_SOURCE),
                )
            )
        if self.story_flags.get("hint:bastian") == "success":
            choices.append(
                make_choice(
                    "royal:accuse_bastian",
                    get_text(SYSTEM_TEXTS, "choice_royal_accuse_bastian", SYSTEM_TEXT_SOURCE),
                )
            )
        return choices

    def _council_choices(self) -> list[Choice]:
        choices = [
            make_choice("council:hof", get_text(SYSTEM_TEXTS, "choice_council_hof", SYSTEM_TEXT_SOURCE)),
            make_choice("council:gilde", get_text(SYSTEM_TEXTS, "choice_council_gilde", SYSTEM_TEXT_SOURCE)),
            make_choice("council:gesandtschaft", get_text(SYSTEM_TEXTS, "choice_council_gesandtschaft", SYSTEM_TEXT_SOURCE)),
            make_choice("council:balanced", get_text(SYSTEM_TEXTS, "choice_council_balanced", SYSTEM_TEXT_SOURCE)),
        ]
        for flag, choice_data in BONUS_COUNCIL_CHOICES.items():
            if self.story_flags.get(flag) == "success":
                choice_id, text_key = choice_data
                choices.append(make_choice(choice_id, get_text(SYSTEM_TEXTS, text_key, SYSTEM_TEXT_SOURCE)))
        return choices

    def _royal_choice_ids(self) -> list[str]:
        return [choice["choice_id"] for choice in self._royal_choices()]

    def _council_choice_ids(self) -> list[str]:
        return [choice["choice_id"] for choice in self._council_choices()]

    def _talk_text(self, npc_id: str) -> str:
        return get_text(NPC_TEXTS[npc_id], "talk", NPC_TEXT_SOURCES[npc_id])

    def _update_goal_status_after_talk(self, npc_id: str, alliance: str) -> None:
        if self.player.player_class is Class.AUFSTEIGER:
            own_alliance = SPECIES_ALLIANCES[self.player.species]
            if alliance == own_alliance:
                self.player.goal_status = self._status_text(
                    get_text(SYSTEM_TEXTS, "status_aufsteiger_contact", SYSTEM_TEXT_SOURCE)
                )
            else:
                self.player.goal_status = self._status_text(
                    get_text(SYSTEM_TEXTS, "status_aufsteiger_missing", SYSTEM_TEXT_SOURCE)
                )

        if self.player.player_class is Class.NETZWERKER:
            npc_species = NPC_SPECIES[npc_id]
            if npc_species in _network_target_species(self.player.species):
                self.network_contact = True
                self.player.goal_status = self._status_text(
                    get_text(SYSTEM_TEXTS, "status_netzwerker_contact", SYSTEM_TEXT_SOURCE)
                )

    def _choose_winning_alliance(self) -> str:
        return self.supported_alliance

    def _evaluate_goal(self) -> None:
        if self.player.player_class is Class.AUFSTEIGER:
            own_alliance = SPECIES_ALLIANCES[self.player.species]
            if self.winning_alliance in (own_alliance, "balanced"):
                self.player.goal_status = "Erreicht: Deine Spezies ist Teil der Allianz mit Schürfrechten."
            else:
                self.player.goal_status = "Verfehlt: Deine Spezies gehört nicht zur siegreichen Allianz."

        elif self.player.player_class is Class.INTRIGANT:
            rival = _rival_species(self.player.species)
            rival_alliance = SPECIES_ALLIANCES[rival]
            if self.rival_blocked or self.winning_alliance != rival_alliance:
                self.player.goal_status = "Erreicht: Dein Rivale bleibt außerhalb der entscheidenden Allianz."
            else:
                self.player.goal_status = "Verfehlt: Dein Rivale bleibt politisch im Spiel."

        elif self.player.player_class is Class.NETZWERKER:
            if self.network_contact and self.royal_contact:
                self.player.goal_status = "Erreicht: Deine neue Verbindung öffnet dir den Weg zum Königspaar."
            elif self.royal_contact:
                self.player.goal_status = "Verfehlt: Du hast das Königspaar erreicht, aber keine passende neue Freundschaft aufgebaut."
            else:
                self.player.goal_status = "Verfehlt: Du hast keine Person des Königspaars direkt erreicht."

    def _run_observation_check(self, choice_id: str) -> str:
        check_data = OBSERVATION_CHECKS.get(choice_id)
        if check_data is None:
            return ""

        attribute, difficulty, flag, success_key, failure_key = check_data
        check = make_attribute_check(self.player, attribute, difficulty)
        if check["success"]:
            self.story_flags[flag] = "success"
            result_text = get_text(SYSTEM_TEXTS, success_key, SYSTEM_TEXT_SOURCE)
        else:
            result_text = get_text(SYSTEM_TEXTS, failure_key, SYSTEM_TEXT_SOURCE)

        return format_attribute_check(check) + "\n" + result_text

    def _council_check_text(self, choice_id: str) -> str:
        attribute = COUNCIL_ATTRIBUTES[self.supported_alliance]
        normal_choices = ("council:hof", "council:gilde", "council:gesandtschaft", "council:balanced")
        difficulty = 5 if choice_id in normal_choices else 4
        check = make_attribute_check(self.player, attribute, difficulty)
        result_key = "council_check_success" if check["success"] else "council_check_failure"
        return format_attribute_check(check) + "\n" + get_text(SYSTEM_TEXTS, result_key, SYSTEM_TEXT_SOURCE)

    def _council_text(self, choice_id: str) -> str:
        if choice_id == "council:gilde_safety":
            base_text = get_text(SYSTEM_TEXTS, "council_gilde_safety", SYSTEM_TEXT_SOURCE)
        elif choice_id == "council:gesandtschaft_rights":
            base_text = get_text(SYSTEM_TEXTS, "council_gesandtschaft_rights", SYSTEM_TEXT_SOURCE)
        elif choice_id == "council:balanced_documents":
            base_text = get_text(SYSTEM_TEXTS, "council_balanced_documents", SYSTEM_TEXT_SOURCE)
        elif self.winning_alliance == "balanced":
            base_text = get_text(SYSTEM_TEXTS, "council_balanced", SYSTEM_TEXT_SOURCE)
        else:
            label = ALLIANCE_LABELS[self.winning_alliance]
            base_text = format_text(SYSTEM_TEXTS, "council_default", SYSTEM_TEXT_SOURCE, alliance_label=label)

        return base_text + "\n\n" + self._council_check_text(choice_id)

    def _status_text(self, text: str) -> str:
        return format_text(SYSTEM_TEXTS, "status_prefix", SYSTEM_TEXT_SOURCE, text=text)

    def _personal_ending_text(self, success: bool) -> str:
        if self.player.player_class is Class.AUFSTEIGER:
            if success:
                return get_text(SYSTEM_TEXTS, "ending_aufsteiger_success", SYSTEM_TEXT_SOURCE)
            return get_text(SYSTEM_TEXTS, "ending_aufsteiger_failure", SYSTEM_TEXT_SOURCE)

        if self.player.player_class is Class.INTRIGANT:
            if success:
                return get_text(SYSTEM_TEXTS, "ending_intrigant_success", SYSTEM_TEXT_SOURCE)
            return get_text(SYSTEM_TEXTS, "ending_intrigant_failure", SYSTEM_TEXT_SOURCE)

        if success:
            return get_text(SYSTEM_TEXTS, "ending_netzwerker_success", SYSTEM_TEXT_SOURCE)
        return get_text(SYSTEM_TEXTS, "ending_netzwerker_failure", SYSTEM_TEXT_SOURCE)
