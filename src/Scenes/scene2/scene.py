from __future__ import annotations
from enum import Enum

from src.Utils import make_response, make_choice
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


def _species_label(species: Species) -> str:
    return species.get_label()


def _overview_text() -> str:
    return (
        "Du lässt deinen Blick durch den Ballsaal wandern. Der Hof hat die Feier "
        "nicht aus Freundlichkeit ausgerichtet. Heute Abend wird entschieden, wer "
        "die neu entdeckte Kristallhöhle im Nordgrat erschließen darf. Unter "
        "den Gesprächen liegt eine zweite Frage: Wer trägt die Schuld, wenn die "
        "Tiefe gefährlicher ist als versprochen?\n\n"
        "Herzogin Alena von Falkenruh spricht für den alten Menschenadel. Sie "
        "will die Schürfrechte unter königlicher Aufsicht halten und fürchtet, "
        "dass eine zu starke Gilde den Hof erpressbar macht. Noch mehr fürchtet "
        "sie einen Vertrag, den der Hof später nicht mehr brechen kann.\n\n"
        "Graf Bastian von Eisenmark lächelt breit, doch seine Worte sind scharf. "
        "Er will schnelle Verträge, schnelle Wagen und schnelle Gewinne. Wer ihm "
        "im Weg steht, wird öffentlich als Feigling dargestellt. Für ihn ist "
        "Zögern fast schon Verrat.\n\n"
        "Meisterin Runa Steinhand vertritt die zwergische Gilde. Sie spricht "
        "von Stützbalken, Wasseradern und Arbeiterrechten. Ohne ihre Leute kommt "
        "niemand tief genug in die Höhle. Sie wirkt, als hätte sie schon etwas "
        "gesehen, das andere lieber überhören.\n\n"
        "Lord Caelion Silberblatt führt die elfische Gesandtschaft. Er warnt, "
        "dass die Höhle in alten Grenzverträgen erwähnt wird. Für ihn ist sie "
        "nicht nur Erz, sondern ein politisches Versprechen, das die Krone "
        "vielleicht vergessen wollte.\n\n"
        "Hofsekretär Marik Voss trägt die alten Urkunden des Reiches. Er wirkt "
        "unscheinbar, aber jede Partei versucht herauszufinden, welche Rolle in "
        "seiner Mappe den Ausschlag geben könnte. Seine Hände zittern nur dann, "
        "wenn jemand die ältesten Siegel erwähnt."
    )


def _observation_text(choice_id: str) -> str:
    texts: dict[str, str] = {
        "observe:alena": (
            "Alena steht am Rand der Tanzfläche und unterhält sich mit zwei "
            "Baronen. Sie sagt: \"Eine Höhle kann ein Reich nähren oder "
            "vergiften. Wer nur den ersten Wagen Erz sieht, sollte keinen "
            "Schlüssel zu ihr bekommen.\"\n\n"
            "Als Bastian lacht, schließt sie für einen Moment die Hand um ihren "
            "Siegelring. Du merkst: Alena sucht Verbündete, aber sie duldet "
            "keine lauten Abenteurer. Wer ihr hilft, muss Ruhe und "
            "Verlässlichkeit zeigen."
        ),
        "observe:bastian": (
            "Bastian hebt seinen Becher und erzählt so laut, dass auch entfernte "
            "Gäste zuhören. \"Der Nordgrat schläft seit Jahrhunderten. Ich sage: "
            "Wecken wir ihn auf. Wer jetzt zögert, wird morgen um Arbeit betteln.\"\n\n"
            "Mehrere junge Adelige lachen. Runa Steinhand verzieht keine Miene. "
            "Caelion merkt sich jedes Wort. Bastian merkt ebenfalls, wer nicht "
            "lacht."
        ),
        "observe:runa": (
            "Runa zeigt einer kleinen Gruppe eine Erzprobe. \"Das ist kein "
            "gewöhnlicher Stein. Wer dort falsch sprengt, bringt den halben Hang "
            "zum Rutschen.\" Dann klappt sie ihr Notizbuch zu.\n\n"
            "Eine junge Dienerin neben ihr wird blass, als Runa von Wasseradern "
            "spricht. Du erkennst: Runa lässt sich durch Höflichkeit gewinnen, "
            "aber nicht durch leere Versprechen."
        ),
        "observe:caelion": (
            "Caelion spricht mit einem Sänger, als ginge es um Musik. Doch seine "
            "Fragen handeln von alten Wegen, verbotenen Quellen und Namen, die "
            "seit Jahren niemand mehr ausspricht.\n\n"
            "Er sagt leise: \"Manchmal ist eine Grenze nicht auf einer Karte, "
            "sondern in einer Erinnerung.\" Als er das sagt, blickt er kurz zu "
            "Mariks Mappe."
        ),
        "observe:marik": (
            "Marik Voss sortiert seine Schriftrollen immer wieder neu. Als "
            "Bastians Name fällt, legt er eine rote Schnur um eine Urkunde. Als "
            "Runa vorbeigeht, schiebt er eine zweite Rolle nach vorn.\n\n"
            "Du bist sicher: Marik weiß, dass die Entscheidung komplizierter ist, "
            "als der Hof offiziell zugibt. Und du bist nicht sicher, ob er diese "
            "Wahrheit freiwillig sagen darf."
        ),
    }
    return texts[choice_id]


def _first_observation_memory(npc_id: str) -> str:
    texts = {
        "alena": (
            "Du erinnerst dich an Alenas Hand am Siegelring. Hinter jedem "
            "freundlichen Satz liegt ihre Angst vor einem Vertrag, der den Hof "
            "fesselt."
        ),
        "bastian": (
            "Du erinnerst dich daran, wie Bastian auch die Gäste zählte, die "
            "nicht lachten. Wer ihn bremst, wird für ihn schnell zum Gegner."
        ),
        "runa": (
            "Du erinnerst dich an Runas Warnung vor Wasseradern. In diesem Streit "
            "geht es nicht nur um Besitz, sondern um Menschen, die später in die "
            "Tiefe steigen müssen."
        ),
        "caelion": (
            "Du erinnerst dich an Caelions Blick zu Mariks Mappe. Alte Verträge "
            "sind heute Abend keine Fußnote, sondern eine Waffe."
        ),
        "marik": (
            "Du erinnerst dich an Mariks zitternde Hände. Irgendetwas in seiner "
            "Mappe ist gefährlich genug, dass alle Seiten es kontrollieren wollen."
        ),
    }
    return texts.get(npc_id, "")


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
            "Das schwere Tor zum Königshof öffnet sich. Hinter dir bleibt die "
            "kalte Nacht, vor dir liegt der Saal voller Licht, Musik und "
            "berechnender Blicke.\n\n"
            f"Ein Herold schlägt mit seinem Stab auf den Boden. \"{self.player.title} "
            f"{self.player.name} ist eingetroffen!\"\n\n"
            "Heute geht es nicht nur um Tanz. Die Kristallhöhle im Nordgrat wurde "
            "entdeckt, und das Königspaar will am Ende des Abends verkünden, "
            "welche Allianz die Schürfrechte erhält. Manche Gäste reden von "
            "Reichtum. Andere reden leiser, wenn sie von der Tiefe sprechen.\n\n"
            "Dein persönliches Ziel bleibt bis dahin im Hintergrund. Erst wenn "
            "die Kerzen heruntergebrannt sind, zeigt sich, ob du erfolgreich warst.",
            input_mode=InputMode.CHOICE,
            choices=[make_choice("continue:look_around", "Die wichtigsten Gäste beobachten")],
            character=self.player.get_character_data(),
            title="Ankunft im Ballsaal",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-arrival",
        )

    def handle_text_input(self, text: str) -> GameResponse:
        return self._response_for_current_step("Bitte wähle eine der angezeigten Optionen.")

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
            "Der Abend ist abgeschlossen.",
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
            return self._response_for_current_step("Diese Auswahl ist hier nicht möglich.")

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
                "Nachdem du genug gesehen hast, wird der Saal enger. Diener "
                "bringen kleine Gläser mit Gewürzwein. Die Musik wird leiser, "
                "damit die Gäste einander besser belauern können.\n\n"
                f"{memory_text}\n\n"
                "Jetzt musst du entscheiden, mit wem du wirklich sprichst. Dieses "
                "Gespräch kann später beeinflussen, welche Allianz stark genug "
                "wird und ob dein eigenes Ziel greifbar bleibt.",
                input_mode=InputMode.CHOICE,
                choices=self._talk_choices(),
                character=self.player.get_character_data(),
                title="Erstes Gespräch",
                msg_type=GameMsgType.QUESTION,
                msg_id="game-ballroom-first-talk-start",
            )

        if choice_id not in self._observation_choice_ids():
            return self._response_for_current_step("Diese Person kannst du gerade nicht auswählen.")

        if choice_id in self.observed_choices:
            return self._response_for_current_step("Diese Person hast du schon beobachtet.")

        self.observed_choices.append(choice_id)
        text = _observation_text(choice_id)
        if len(self.observed_choices) == 1:
            self.story_flags["first_observed_npc"] = choice_id.removeprefix("observe:")

        if len(self.observed_choices) >= 3:
            text += (
                "\n\nDu hast genug Hinweise gesammelt, um ein erstes Gespräch "
                "zu wagen. Du kannst noch weiter beobachten oder dich direkt "
                "unter die entscheidenden Gäste mischen."
            )

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
        talk_targets = {
            "talk:alena": ("alena", "hof"),
            "talk:bastian": ("bastian", "hof"),
            "talk:runa": ("runa", "gilde"),
            "talk:caelion": ("caelion", "gesandtschaft"),
            "talk:marik": ("marik", "balanced"),
        }
        if choice_id not in talk_targets:
            return self._response_for_current_step("Diese Gesprächspartnerin oder diesen Gesprächspartner gibt es hier nicht.")

        npc_id, alliance = talk_targets[choice_id]
        self.talked_to = npc_id
        self.supported_alliance = alliance
        self._update_goal_status_after_talk(npc_id, alliance)
        self.step = BallroomStep.ROYAL_INTERMEZZO
        return make_response(
            self._talk_text(npc_id)
            + "\n\nEin Gong unterbricht die Gespräche. Königin Meridia tritt "
            "auf die oberste Stufe der Marmortreppe. Neben ihr steht König "
            "Arwed, blass und aufmerksam. Die Königin hebt die Hand, und selbst "
            "Bastian verstummt.\n\n"
            "\"Viele von Euch sprechen heute von Rechten\", sagt Meridia. "
            "\"Ich will wissen, wer auch von Verantwortung spricht. Vor der "
            "letzten Beratung höre ich genau eine Stimme aus dem Saal.\"",
            input_mode=InputMode.CHOICE,
            choices=self._royal_choices(),
            character=self.player.get_character_data(),
            title="Gespräch",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-talk",
        )

    def _handle_royal_intermezzo(self, choice_id: str) -> GameResponse:
        if choice_id not in ("royal:speak", "royal:listen", "royal:accuse"):
            return self._response_for_current_step("Diese Auswahl ist hier nicht möglich.")

        if choice_id == "royal:speak":
            self.royal_contact = True
            self.player.goal_status = self._status_text("Du hast mit Königin Meridia gesprochen.")
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            text = (
                "Du trittst vor und sprichst die Königin direkt an. Du formulierst "
                "keine Forderung, sondern bietest eine Beobachtung an: Die Höhle "
                "braucht mehr als Besitzansprüche. Sie braucht Vertrauen zwischen "
                "den Leuten, die dort arbeiten, und denen, die darüber regieren.\n\n"
                f"{memory_text}\n\n"
                "Meridia sieht dich lange an. Dann sagt sie: \"Eine seltene "
                "Antwort an einem Abend voller Hunger.\""
            )
        elif choice_id == "royal:accuse":
            self.rival_blocked = True
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            text = (
                "Du nutzt den Moment für einen Angriff. Du erwähnst Widersprüche "
                "in den Aussagen deines Rivalen und zwingst Marik, eine passende "
                "Urkunde vorzulesen. Der Saal wird still.\n\n"
                f"{memory_text}\n\n"
                "Die betroffene Partei verliert sichtbar an Gewicht. Niemand wird "
                "aus dem Saal geworfen, aber einige Türen schließen sich leise."
            )
        else:
            memory_text = _first_observation_memory(self.story_flags.get("first_observed_npc", ""))
            text = (
                "Du bleibst am Rand und hörst zu. Die Königin fragt nicht nach "
                "Schmeichelei, sondern nach Folgen: Wer trägt Verantwortung, wenn "
                "die erste Mine einstürzt? Wer ersetzt zerstörte Quellen? Wer "
                "spricht für Arbeiter, Händler und Grenzorte?\n\n"
                f"{memory_text}\n\n"
                "Deine Zurückhaltung verschafft dir kein Gespräch mit dem "
                "Königspaar, aber du lernst, welche Argumente im Rat zählen."
            )

        self.step = BallroomStep.COUNCIL
        return make_response(
            text
            + "\n\nDanach öffnen sich die Türen zum kleinen Ratssaal. Nicht alle "
            "Gäste dürfen hinein, aber deine Einladung reicht. Drinnen warten "
            "keine Tänze mehr, nur Tinte, Siegel und Menschen, die einander mit "
            "leiser Stimme drohen.",
            input_mode=InputMode.CHOICE,
            choices=self._council_choices(),
            character=self.player.get_character_data(),
            title="Vor dem Königspaar",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-royal",
        )

    def _handle_council(self, choice_id: str) -> GameResponse:
        if choice_id not in ("council:hof", "council:gilde", "council:gesandtschaft", "council:balanced"):
            return self._response_for_current_step("Diese Ratsentscheidung ist nicht möglich.")

        self.supported_alliance = choice_id.removeprefix("council:")
        self.winning_alliance = self._choose_winning_alliance()
        self._evaluate_goal()
        self.step = BallroomStep.FINAL
        return make_response(
            self._council_text()
            + "\n\nDie Beratung dauert länger, als alle erwartet haben. Einmal "
            "fällt ein Glas um, und niemand lacht. Als die Türen wieder aufgehen, "
            "sind die Kerzen kurz vor dem Erlöschen. Der Ball ist fast vorbei, "
            "aber die Verkündung steht noch aus.",
            input_mode=InputMode.CHOICE,
            choices=[make_choice("continue:ending", "Die Verkündung anhören")],
            character=self.player.get_character_data(),
            title="Ratssaal",
            msg_type=GameMsgType.QUESTION,
            msg_id="game-ballroom-council",
        )

    def _handle_final(self, choice_id: str) -> GameResponse:
        if choice_id != "continue:ending":
            return self._response_for_current_step("Diese Auswahl ist hier nicht möglich.")

        self.step = BallroomStep.DONE
        success = self.player.goal_status.startswith("Erreicht")
        result = self._personal_ending_text(success)
        return make_response(
            f"König Arwed erhebt sich. \"Die Schürfrechte gehen an die "
            f"{ALLIANCE_LABELS[self.winning_alliance]}. Keine Seite erhält alles, "
            "aber eine Seite trägt ab morgen die Verantwortung. Und wer "
            "Verantwortung trägt, kann sich nicht mehr hinter Gerüchten "
            "verstecken.\"\n\n"
            "Im Saal brechen Gespräche los. Alena prüft sofort die Formulierungen "
            "des Vertrags. Bastian lächelt nur noch mit den Zähnen. Runa fragt "
            "nach Karten und Arbeitern. Caelion lässt sich jedes Siegel zeigen. "
            "Marik wirkt zum ersten Mal an diesem Abend erleichtert.\n\n"
            f"{result}\n\n"
            f"Zielstatus: {self.player.goal_status}\n\n"
            "Der Abend endet nicht mit einem Kampf, sondern mit Unterschriften, "
            "verletztem Stolz und neuen Bündnissen. Als du den Hof verlässt, "
            "liegt der Nordgrat noch immer dunkel am Horizont. Die Höhle ist "
            "nicht weniger gefährlich geworden. Nur die Namen der Menschen, die "
            "sich ihr stellen müssen, stehen nun fest.",
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
            choices = [make_choice("continue:ending", "Die Verkündung anhören")]
        else:
            choices = [make_choice("continue:look_around", "Die wichtigsten Gäste beobachten")]

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
        return ["observe:alena", "observe:bastian", "observe:runa", "observe:caelion", "observe:marik"]

    def _observation_choices(self) -> list[Choice]:
        labels = {
            "observe:alena": "Herzogin Alena beobachten",
            "observe:bastian": "Graf Bastian beobachten",
            "observe:runa": "Meisterin Runa beobachten",
            "observe:caelion": "Lord Caelion beobachten",
            "observe:marik": "Hofsekretär Marik beobachten",
        }
        choices = [
            make_choice(choice_id, label)
            for choice_id, label in labels.items()
            if choice_id not in self.observed_choices
        ]
        if len(self.observed_choices) >= 3:
            choices.append(make_choice("continue:first_talk", "Ein Gespräch beginnen"))
        return choices

    def _talk_choices(self) -> list[Choice]:
        return [
            make_choice("talk:alena", "Mit Herzogin Alena sprechen"),
            make_choice("talk:bastian", "Mit Graf Bastian sprechen"),
            make_choice("talk:runa", "Mit Meisterin Runa sprechen"),
            make_choice("talk:caelion", "Mit Lord Caelion sprechen"),
            make_choice("talk:marik", "Mit Hofsekretär Marik sprechen"),
        ]

    def _royal_choices(self) -> list[Choice]:
        return [
            make_choice("royal:speak", "Selbst vor der Königin sprechen"),
            make_choice("royal:listen", "Zuhören und Informationen sammeln"),
            make_choice("royal:accuse", "Den Rivalen öffentlich schwächen"),
        ]

    def _council_choices(self) -> list[Choice]:
        return [
            make_choice("council:hof", "Die königliche Hofallianz unterstützen"),
            make_choice("council:gilde", "Den Gildenpakt unterstützen"),
            make_choice("council:gesandtschaft", "Die elfische Gesandtschaft unterstützen"),
            make_choice("council:balanced", "Einen gemeinsamen Kronenpakt vorschlagen"),
        ]

    def _talk_text(self, npc_id: str) -> str:
        texts = {
            "alena": (
                "Alena hört dir zu, ohne dich zu unterbrechen. \"Viele kommen "
                "heute mit offenen Händen\", sagt sie. \"Die meisten haben darin "
                "schon einen Vertrag versteckt. Sagt mir: Wollt Ihr Ordnung oder "
                "nur einen Anteil?\"\n\n"
                "Du antwortest vorsichtig. Alena nickt, als du erwähnst, dass "
                "ein Schürfrecht ohne Kontrolle nur den nächsten Streit vorbereitet. "
                "Zum ersten Mal wirkt sie nicht freundlich, sondern ehrlich müde."
            ),
            "bastian": (
                "Bastian schlägt dir freundschaftlich auf die Schulter, etwas zu "
                "fest. \"Endlich jemand, der nicht nur flüstert. Die Höhle wird "
                "reich machen, wer den Mut hat, zuerst hineinzugehen.\"\n\n"
                "Sein Lachen klingt offen, aber seine Augen prüfen, ob du nützlich "
                "oder gefährlich bist. Als du nicht sofort zustimmst, wird sein "
                "Lächeln eine Spur schmaler."
            ),
            "runa": (
                "Runa legt die Erzprobe in deine Hand. Sie ist schwerer, als sie "
                "aussieht. \"Wer über Schürfrechte spricht, soll wissen, was ein "
                "gebrochener Stollen kostet\", sagt sie.\n\n"
                "Als du nach Arbeitern, Wasser und Karten fragst, wird ihre Stimme "
                "wärmer. Sie merkt, dass du ihr Handwerk ernst nimmst. Dann sagt "
                "sie leise: \"Die Höhle wird nicht warten, bis der Hof fertig "
                "gestritten hat.\""
            ),
            "caelion": (
                "Caelion begrüßt dich mit einer knappen Verbeugung. \"Der Hof "
                "nennt die Höhle neu, weil er sie neu gefunden hat. Das ist nicht "
                "dasselbe.\"\n\n"
                "Er erzählt von einem alten Grenzbaum, von einem verschwundenen "
                "Siegel und von Liedern, die nur noch ältere Elfen kennen. Seine "
                "Stimme bleibt ruhig, aber seine Worte stellen den ganzen Abend "
                "auf unsicheren Boden."
            ),
            "marik": (
                "Marik wirkt erleichtert, als du nicht sofort eine Forderung "
                "stellst. \"Alle wollen wissen, was in meinen Rollen steht\", "
                "murmelt er. \"Kaum jemand fragt, warum der König sie heute erst "
                "zeigen lässt.\"\n\n"
                "Er verrät dir, dass keine Partei allein einen sauberen Anspruch "
                "hat. Das macht einen gemeinsamen Pakt möglich. Als er das sagt, "
                "blickt er zur Treppe, als fürchte er, schon zu viel gesagt zu "
                "haben."
            ),
        }
        return texts[npc_id]

    def _update_goal_status_after_talk(self, npc_id: str, alliance: str) -> None:
        if self.player.player_class is Class.AUFSTEIGER:
            own_alliance = SPECIES_ALLIANCES[self.player.species]
            if alliance == own_alliance:
                self.player.goal_status = self._status_text("Du hast Kontakt zu deiner Spezies-Allianz.")
            else:
                self.player.goal_status = self._status_text("Du hast noch keinen sicheren Platz in deiner Spezies-Allianz.")

        if self.player.player_class is Class.NETZWERKER:
            npc_species = {
                "alena": Species.HUMAN,
                "bastian": Species.HUMAN,
                "runa": Species.DWARF,
                "caelion": Species.ELF,
                "marik": Species.HUMAN,
            }[npc_id]
            if npc_species in _network_target_species(self.player.species):
                self.network_contact = True
                self.player.goal_status = self._status_text("Du hast eine passende neue Bekanntschaft geknüpft.")

    def _choose_winning_alliance(self) -> str:
        if self.supported_alliance == "balanced" and self.player.attributes[Attributes.UNDERSTANDING] >= 3:
            return "balanced"
        if self.supported_alliance == "gilde" and self.player.attributes[Attributes.KNOWLEDGE] >= 3:
            return "gilde"
        if self.supported_alliance == "hof" and self.player.attributes[Attributes.WIT] >= 3:
            return "hof"
        if self.supported_alliance == "gesandtschaft" and self.player.attributes[Attributes.UNDERSTANDING] >= 3:
            return "gesandtschaft"
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

    def _council_text(self) -> str:
        label = ALLIANCE_LABELS[self.winning_alliance]
        if self.winning_alliance == "balanced":
            return (
                "Du schlägst einen Kronenpakt vor: Die Krone hält das letzte "
                "Siegel, die Gilde leitet die Arbeit, die Gesandtschaft prüft "
                "alte Grenzen und der Hof wacht über Steuern und Sicherheit.\n\n"
                "Der Vorschlag ist unbequem, weil niemand alles bekommt. Gerade "
                "deshalb wird es still. Alena hasst die geteilte Kontrolle, "
                "Bastian hasst die Verzögerung, Runa hasst die höfischen Worte, "
                "und Caelion hasst, dass er trotzdem zuhören muss."
            )

        return (
            f"Du stellst dich im Rat deutlich hinter die {label}. Deine Worte "
            "werden nicht allein entscheiden, aber sie geben einer Seite genau "
            "in dem Moment Gewicht, in dem Marik die alten Ansprüche vorliest.\n\n"
            "Es wird gestritten, gezählt, verbessert und gedroht. Marik liest "
            "eine Zeile zweimal, weil beim ersten Mal zu viele Gäste gleichzeitig "
            "widersprechen. Am Ende erkennt man an den Gesichtern, wohin sich "
            "die Entscheidung neigt."
        )

    def _status_text(self, text: str) -> str:
        return f"Zwischenstand: {text}"

    def _personal_ending_text(self, success: bool) -> str:
        if self.player.player_class is Class.AUFSTEIGER:
            if success:
                return (
                    "Du warst erfolgreich. Dein Name wird morgen nicht in den "
                    "großen Verträgen stehen, aber er wird in den richtigen "
                    "Gesprächen fallen."
                )
            return (
                "Du hast dein Ziel nicht erreicht. Als die Sieger einander "
                "zunicken, merkst du, dass dein Platz am Rand des Saals noch "
                "nicht verschwunden ist."
            )

        if self.player.player_class is Class.INTRIGANT:
            if success:
                return (
                    "Du warst erfolgreich. Dein Rivale verlässt den Saal mit "
                    "gesenkter Stimme. Niemand nennt dich als Ursache, und genau "
                    "das macht deinen Sieg wertvoll."
                )
            return (
                "Du hast dein Ziel nicht erreicht. Dein Rivale bleibt im Spiel "
                "und lächelt, als hätte er den Abend besser verstanden als du."
            )

        if success:
            return (
                "Du warst erfolgreich. Die neue Verbindung ist noch kein Bündnis, "
                "aber sie hat dir einen Weg zum Königspaar geöffnet."
            )
        return (
            "Du hast dein Ziel nicht erreicht. Du hast Stimmen gehört und Namen "
            "gesammelt, doch keine Verbindung wurde stark genug, um eine Tür zu "
            "öffnen."
        )
