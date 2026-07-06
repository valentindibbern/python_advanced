from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from src.Classes.PC import PC
from src.Classes.Scene import Choice
from src.Enums.Attributes import Attributes
from src.Enums.InputMode import InputMode

if TYPE_CHECKING:
    from src.Classes.Game import GameResponse


class BallroomArrivalStep(Enum):
    ARRIVAL = 0
    NPC_OVERVIEW = 1
    FIRST_OBSERVATION = 2
    DONE = 3


class BallroomArrivalScene:
    def __init__(self, player: PC, story_flags: dict[str, str]) -> None:
        self.scene_id = "1"
        self.player = player
        self.story_flags = story_flags
        self.step = BallroomArrivalStep.ARRIVAL
        self.selected_npc_ids: list[str] = []

    def start(self) -> GameResponse:
        self.step = BallroomArrivalStep.ARRIVAL
        player_name = self.player.name
        species = self._get_species_label()
        player_class = self._get_class_label()

        return self._make_response(
            "Ankunft im Ballsaal\n\n"
            "Das schwere Tor zum Königshof öffnet sich langsam. Dahinter liegt der "
            "grosse Saal, hell erleuchtet von Kerzen und Spiegeln. Stimmen, Schritte "
            "und leise Musik vermischen sich zu einem unruhigen Klang.\n\n"
            "Zwei Wachen prüfen deine Einladung. Dann tritt ein Angestellter in "
            "dunkelroter Hofkleidung vor, sieht kurz auf seine Liste und hebt die "
            "Stimme.\n\n"
            f"\"{player_name}, {species}, bekannt als {player_class}, ist eingetroffen!\"\n\n"
            "Für einen Moment richten sich mehrere Blicke auf dich. Manche wirken "
            "neugierig, manche berechnend, andere wenden sich sofort wieder ihren "
            "Gesprächen zu. Überall im Saal wird über die neu entdeckte Höhle "
            "und das Schürfrecht gesprochen.",
            input_mode=InputMode.CHOICE,
            choices = [{"id": "continue:look_around", "label": "Dich im Saal umsehen"}],
            character=self._get_character_data(),
        )

    def handle_text_input(self, text: str) -> GameResponse:
        return self._response_for_current_step("Bitte wähle eine der angezeigten Optionen.")

    def handle_choice(self, choice_id: str) -> GameResponse:
        if self.step == BallroomArrivalStep.ARRIVAL:
            return self._handle_arrival_choice(choice_id)

        if self.step == BallroomArrivalStep.NPC_OVERVIEW:
            return self._handle_npc_choice(choice_id)

        if self.step == BallroomArrivalStep.FIRST_OBSERVATION:
            return self._handle_end_choice(choice_id)

        return self._make_response(
            "Der Abend im Ballsaal geht weiter.",
            input_mode=InputMode.NONE,
            character=self._get_character_data(),
        )

    def is_done(self) -> bool:
        return self.step == BallroomArrivalStep.DONE

    def get_player(self) -> PC | None:
        return self.player

    def _handle_arrival_choice(self, choice_id: str) -> GameResponse:
        if choice_id != "continue:look_around":
            return self._response_for_current_step("Diese Auswahl ist hier nicht möglich.")

        self.step = BallroomArrivalStep.NPC_OVERVIEW
        self.selected_npc_ids = []
        return self._make_response(
            self._get_npc_overview_text(),
            input_mode=InputMode.CHOICE,
            choices=self._get_npc_choices(),
            character=self._get_character_data(),
        )

    def _handle_npc_choice(self, choice_id: str) -> GameResponse:
        observations = self._get_npc_observations()

        if choice_id not in observations:
            return self._response_for_current_step("Diese Person kannst du gerade nicht auswählen.")

        if choice_id in self.selected_npc_ids:
            return self._response_for_current_step("Diese Person hast du schon beobachtet.")

        flag_value, text = observations[choice_id]
        if "first_observed_npc" not in self.story_flags:
            self.story_flags["first_observed_npc"] = flag_value

        self.selected_npc_ids.append(choice_id)

        if len(self.selected_npc_ids) == len(observations):
            self.step = BallroomArrivalStep.FIRST_OBSERVATION
            return self._make_response(
                text + "\n\nDu hast alle wichtigen Personen im Ballsaal beobachtet.",
                input_mode=InputMode.CHOICE,
                choices=[
                    {"id": "continue:end_scene", "label": "Dich unter die Gäste mischen"},
                ],
                character=self._get_character_data(),
            )

        return self._make_response(
            text,
            input_mode=InputMode.CHOICE,
            choices=self._get_npc_choices(),
            character=self._get_character_data(),
        )

    def _handle_end_choice(self, choice_id: str) -> GameResponse:
        if choice_id != "continue:end_scene":
            return self._response_for_current_step("Diese Auswahl ist hier nicht möglich.")

        self.step = BallroomArrivalStep.DONE
        return self._make_response(
            "Du trittst tiefer in den Saal. Die Musik wird lauter, aber die "
            "Gespräche um die Höhle sind überall zu hören. Der Abend hat gerade "
            "erst begonnen.",
            input_mode=InputMode.NONE,
            character=self._get_character_data(),
        )

    def _response_for_current_step(self, text: str) -> GameResponse:
        if self.step == BallroomArrivalStep.ARRIVAL:
            return self._make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=[
                    {"id": "continue:look_around", "label": "Dich im Saal umsehen"},
                ],
                character=self._get_character_data(),
            )

        if self.step == BallroomArrivalStep.NPC_OVERVIEW:
            return self._make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=self._get_npc_choices(),
                character=self._get_character_data(),
            )

        if self.step == BallroomArrivalStep.FIRST_OBSERVATION:
            return self._make_response(
                text,
                input_mode=InputMode.CHOICE,
                choices=[
                    {"id": "continue:end_scene", "label": "Dich unter die Gäste mischen"},
                ],
                character=self._get_character_data(),
            )

        return self._make_response(text, input_mode=InputMode.NONE, character=self._get_character_data())

    def _get_npc_choices(self) -> list[Choice]:
        choices = [
            {"id": "npc:duchess", "label": "Herzogin Alena genauer beobachten"},
            {"id": "npc:count", "label": "Graf Bastian genauer beobachten"},
            {"id": "npc:guildmaster", "label": "Meisterin Runa genauer beobachten"},
            {"id": "npc:envoy", "label": "Lord Caelion genauer beobachten"},
            {"id": "npc:secretary", "label": "Hofsekretär Marik genauer beobachten"},
        ]

        return [choice for choice in choices if choice["id"] not in self.selected_npc_ids]

    def _get_npc_observations(self) -> dict[str, tuple[str, str]]:
        return {
            "npc:duchess": (
                "duchess",
                "Du beobachtest Herzogin Alena genauer. Sie lächelt selten, aber jede "
                "Person in ihrer Nähe senkt unbewusst die Stimme. Sie scheint nicht "
                "nach schnellem Reichtum zu suchen. Ihr Blick wandert immer wieder zu "
                "jenen Adeligen, die zu laut vom Gewinn der Höhle sprechen.\n\n"
                "Dir wird klar: Alena will Kontrolle. Wenn das Schürfrecht vergeben "
                "wird, dann soll kein einzelnes Haus stark genug werden, den König "
                "unter Druck zu setzen.",
            ),
            "npc:count": (
                "count",
                "Du richtest deine Aufmerksamkeit auf Graf Bastian. Er spricht mit "
                "offenen Händen, breitem Lächeln und lauter Stimme. Um ihn herum "
                "stehen viele Zuhörer. Einige nicken begeistert, andere wirken eher "
                "eingeschüchtert als überzeugt.\n\n"
                "Dir wird klar: Bastian verkauft die Höhle als Versprechen für "
                "Reichtum und Arbeit. Doch wer ihm folgt, macht sich auch von seinem "
                "Ehrgeiz abhängig.",
            ),
            "npc:guildmaster": (
                "guildmaster",
                "Du lauschst Meisterin Runa Steinhand. Sie redet nicht von Ruhm, "
                "sondern von Stollen, Stützbalken, Wasseradern und Kosten. In ihrer "
                "Hand liegt eine kleine Erzprobe, die sie nur Personen zeigt, denen "
                "sie fachlich vertraut.\n\n"
                "Dir wird klar: Runa will, dass Bergleute und Gilden mitentscheiden. "
                "Sie fürchtet weniger die Höhle selbst als adelige Hast und "
                "schlechte Planung.",
            ),
            "npc:envoy": (
                "envoy",
                "Du beobachtest Lord Caelion Silberblatt. Er spricht leise, doch er "
                "überhört fast nichts. Seine Augen folgen nicht den lautesten "
                "Rednern, sondern den Menschen, die bei bestimmten Namen erschrecken "
                "oder schweigen.\n\n"
                "Dir wird klar: Caelion sucht nach verborgener Angst. Für ihn ist "
                "die Höhle nicht nur eine Quelle von Erz, sondern vielleicht ein Ort "
                "alter Abmachungen und gefährlicher Geheimnisse.",
            ),
            "npc:secretary": (
                "secretary",
                "Du siehst zu Hofsekretär Marik Voss. Er steht nahe bei den Türen "
                "zum inneren Ratssaal und hält mehrere Schriftrollen fest an sich "
                "gedrückt. Als der Name Eisenmark fällt, schiebt er eine Rolle "
                "hastig unter die anderen.\n\n"
                "Dir wird klar: Marik ist offiziell neutral, aber er weiss mehr, als "
                "er gerade sagen darf. Vielleicht kennt er alte Ansprüche, die den "
                "ganzen Abend verändern könnten.",
            ),
        }

    def _get_npc_overview_text(self) -> str:
        return (
            "Du lässt deinen Blick durch den Ballsaal wandern. Zwischen Musik, "
            "Seide, Rüstungsteilen und geduckten Dienern fallen dir mehrere "
            "Personen besonders auf.\n\n"
            "Herzogin Alena von Falkenruh steht nahe einer Marmorsäule. Ihr "
            "dunkelgrünes Kleid ist mit silbernen Stickereien besetzt, doch sie "
            "trägt den Schmuck nicht, um aufzufallen. Ihre Haltung ist gerade, ihr "
            "Blick ruhig und kontrolliert. Politisch steht sie für eine vorsichtige "
            "Nutzung der Höhle unter königlicher Kontrolle. Sie will verhindern, "
            "dass ein einzelnes Adelshaus durch das Schürfrecht zu mächtig wird.\n\n"
            "Graf Bastian von Eisenmark ist kaum zu übersehen. Er ist breitschultrig, "
            "trägt einen dunklen Bart und einen schweren Mantel mit Metallspangen. "
            "Er spricht laut, selbstbewusst und mit sichtbarem Vergnügen. Politisch "
            "fordert er eine schnelle Ausbeutung der Höhle durch starke Adelshäuser. "
            "Er verspricht Reichtum und Arbeit, wirkt aber rücksichtslos gegenüber "
            "Risiken für Arbeiter, kleinere Häuser und das Land selbst.\n\n"
            "Meisterin Runa Steinhand, eine zwergische Gildenmeisterin, steht nicht "
            "in der Mitte des Saals, sondern dort, wo man ernsthafte Gespräche führt. "
            "Ihr graues Haar ist in feste Zöpfe gebunden. Statt höfischem Prunk "
            "trägt sie einfache, hochwertige Kleidung und hält ein kleines Notizbuch "
            "bei sich. Politisch fordert sie, dass Bergleute, Handwerker und Gilden "
            "am Schürfrecht beteiligt werden. Sie misstraut Adeligen, die nur vom "
            "Gewinn sprechen.\n\n"
            "Lord Caelion Silberblatt, ein elfischer Gesandter, wirkt beinahe still "
            "neben all den lauten Stimmen. Sein helles Haar fällt glatt über die "
            "Schultern, an seinem Hals liegt eine schmale goldene Kette. Er beobachtet "
            "viel und spricht wenig. Politisch warnt er vor überstürztem Abbau. Er "
            "befürchtet, dass alte Verträge, verborgene Orte oder diplomatische "
            "Grenzen verletzt werden könnten.\n\n"
            "Hofsekretär Marik Voss steht nahe den Türen zum inneren Ratssaal. Er "
            "ist schmal, sauber gekleidet und hält mehrere Schriftrollen an sich "
            "gedrückt. Sein Blick ist wach, aber nervös. Offiziell ist er neutral. "
            "Tatsächlich kennt er vermutlich Einladungslisten, Besitzansprüche und "
            "alte Abmachungen, die für die Entscheidung über die Höhle wichtig "
            "werden könnten."
        )

    def _get_species_label(self) -> str:
        if self.player.species is None:
            return "unbekannter Herkunft"

        return self.player.species.get_label()

    def _get_class_label(self) -> str:
        if self.player.player_class is None:
            return "Gast des Hofes"

        return self.player.player_class.get_label()

    def _get_character_data(self) -> dict[str, str | int]:
        return {
            "name": self.player.name,
            "species": self._get_species_label(),
            "player_class": self._get_class_label(),
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
