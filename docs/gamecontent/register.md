# Spielinhaltsregister

Dieses Register beschreibt die Begriffe, Szenen, Figuren und Choice-IDs, die
im aktuellen Code verwendet werden.

## Textdateien

Sichtbare Szeneninhalte werden aus festen `.txt`-Dateien geladen. Die
Ladefunktionen stehen in `src/Utils.py`:

- `load_text_blocks()`
- `get_text()`
- `format_text()`
- `require_text_keys()`

Das Format besteht aus Blöcken:

```text
[key]
Text über mehrere Zeilen.
```

Wichtige Regeln:

- Textdateien sind UTF-8.
- Keys dürfen nicht doppelt vorkommen.
- Benötigte Keys werden beim Laden geprüft.
- Platzhalter wie `{name}` werden im Code gefüllt.
- Es gibt keine dynamische Registrierung. Neue Dateien und Keys müssen im Code
  fest eingetragen werden.

Dateien:

- `src/Scenes/scene0/texts/system.txt`: Startbildschirm
- `src/Scenes/scene1/texts/system.txt`: allgemeine Charaktererstellung
- `src/Scenes/scene1/texts/class_*.txt`: Klassenauswahl und Klassentexte
- `src/Scenes/scene1/texts/species_*.txt`: Speziesauswahl und Speziestexte
- `src/Scenes/scene2/texts/system.txt`: Ballsaal, Übergänge, Choices,
  Fehlermeldungen, Rat und Ende
- `src/Scenes/scene2/texts/alena.txt`: Beobachtung, Erinnerung und Gespräch
  zu Alena
- `src/Scenes/scene2/texts/bastian.txt`: Beobachtung, Erinnerung und Gespräch
  zu Bastian
- `src/Scenes/scene2/texts/runa.txt`: Beobachtung, Erinnerung und Gespräch
  zu Runa
- `src/Scenes/scene2/texts/caelion.txt`: Beobachtung, Erinnerung und Gespräch
  zu Caelion
- `src/Scenes/scene2/texts/marik.txt`: Beobachtung, Erinnerung und Gespräch
  zu Marik
- `src/Scenes/scene2/texts/queen.txt`: Notiz zu Königin Meridia
- `src/Scenes/scene2/texts/king.txt`: Notiz zu König Arwed

## Charakterdaten

Die Charakterdaten werden in der UI im Bereich `Charakter` angezeigt.

Felder:

- Name
- Titel
- Spezies
- Klasse
- Wissen
- Schlagfertigkeit
- Verständnis
- Ziel
- Status

Der Titel ist aktuell immer `Baron`. Das Ziel wird nach Klasse und Spezies
gesetzt. Der Status zeigt während des Ballabends Zwischenstände und am Ende
das Ergebnis.

## Klassen und Ziele

Code-Enum: `Class`

| Enum-Wert | Anzeige | Ziel |
| --- | --- | --- |
| `AUFSTEIGER` | Aufsteiger | Die eigene Spezies soll Teil der Allianz mit Schürfrechten sein. |
| `INTRIGANT` | Intrigant | Der Rivale darf nicht Teil der entscheidenden Allianz sein. |
| `NETZWERKER` | Netzwerker | Über eine neue Verbindung eine Person des Königspaars erreichen. |
| `NOTSET` | Nicht gesetzt | kein Ziel |

Erzählerische Rollen:

- Aufsteiger: Der eigene Name soll am Hof mehr Gewicht bekommen.
- Intrigant: Ein Rivale soll geschwächt werden, ohne dass der Spieler offen
  als Ursache sichtbar wird.
- Netzwerker: Ein richtiger Kontakt soll wichtiger sein als eine laute Rede.

Choice-IDs in der Charaktererstellung:

- `class:AUFSTEIGER`
- `class:INTRIGANT`
- `class:NETZWERKER`

## Spezies

Code-Enum: `Species`

| Enum-Wert | Anzeige | Bonus | Politische Gruppe |
| --- | --- | --- | --- |
| `HUMAN` | Mensch | +1 Schlagfertigkeit | königliche Hofallianz |
| `ELF` | Elf | +1 Verständnis | elfische Gesandtschaft |
| `DWARF` | Zwerg | +1 Wissen | Gildenpakt |
| `NOTSET` | Nicht gesetzt | kein Bonus | keine |

Erzählerische Spannungen:

- Mensch: nahe am Hof, aber in Gefallen und Absprachen verstrickt.
- Elf: Träger alter Rechte, denen der Hof misstraut.
- Zwerg: Fachwissen über Stein und Stollen, aber Gefahr, vom Hof nur benutzt
  zu werden.

Choice-IDs in der Charaktererstellung:

- `species:HUMAN`
- `species:ELF`
- `species:DWARF`

## Zielregeln

Aufsteiger:

- Mensch gewinnt, wenn `hof` oder `balanced` die Schürfrechte erhält.
- Zwerg gewinnt, wenn `gilde` oder `balanced` die Schürfrechte erhält.
- Elf gewinnt, wenn `gesandtschaft` oder `balanced` die Schürfrechte erhält.

Intrigant:

- Menschlicher Spieler: Rivale ist ein Mensch.
- Zwergischer Spieler: Rivale ist ein Elf.
- Elfischer Spieler: Rivale ist ein Zwerg.
- Erfolg, wenn der Rivale durch `royal:accuse` geschwächt wird oder wenn die
  Rivalengruppe nicht die siegreiche Allianz ist.

Netzwerker:

- Menschlicher Spieler sucht Kontakt zu einem Zwerg oder Elf.
- Zwergischer oder elfischer Spieler sucht Kontakt zu einem Menschen.
- Erfolg, wenn der Spieler eine passende neue Bekanntschaft schließt und vor
  dem Königspaar `royal:speak` wählt.

## Attribute

Code-Enum: `Attributes`

| Enum-Wert | Anzeige |
| --- | --- |
| `KNOWLEDGE` | Wissen |
| `WIT` | Schlagfertigkeit |
| `UNDERSTANDING` | Verständnis |

Die Startverteilung nutzt das Muster `2, 1, 1`. Danach wird der Speziesbonus
addiert.

Choice-IDs:

- `attributes:KNOWLEDGE`
- `attributes:WIT`
- `attributes:UNDERSTANDING`

## Szene 0: Startbildschirm

Code-Datei: `src/Scenes/scene0/scene.py`

Titel in der UI: `Start`

Zweck:

- Führt den Spieler mit Schnee, Kerzen und Gerüchten über die Kristallhöhle in
  die Stimmung des Ballabends ein.
- Erklärt den Start über den Button `Start`.
- Verweist darauf, dass `Stop` das Fenster schließt.

Wichtige Message-ID:

- `game-start-screen`

## Szene 1: Charaktererstellung

Code-Datei: `src/Scenes/scene1/scene.py`

Titel in der UI: `Charaktererstellung`

Ablauf:

1. Name eingeben
2. Klasse mit persönlicher Motivation wählen
3. Spezies mit politischer Spannung und Bonus wählen
4. Attributverteilung mit kurzer Erklärung wählen
5. Ziel setzen und Charakter abschließen

Wichtige Message-IDs:

- `game-character-name-question`
- `game-character-name-error`
- `game-character-class-question`
- `game-character-species-question`
- `game-character-attributes-question`
- `game-character-created`

## Szene 2: Ballabend

Code-Datei: `src/Scenes/scene2/scene.py`

Titel in der UI:

- `Ankunft im Ballsaal`
- `Die Gäste`
- `Beobachtung`
- `Erstes Gespräch`
- `Gespräch`
- `Vor dem Königspaar`
- `Ratssaal`
- `Ende des Ballabends`

Ablauf:

1. Der Spieler kommt im Ballsaal an.
2. Der Spieler beobachtet mindestens drei wichtige Personen.
3. Der Spieler führt ein erstes politisches Gespräch.
4. Die erste Beobachtung wird als Erinnerung aufgegriffen.
5. Der Spieler reagiert auf den Auftritt des Königspaars.
6. Die erste Beobachtung kann erneut als Erinnerung auftauchen.
7. Der Spieler unterstützt im Rat eine Allianz.
8. Das Königspaar verkündet die Schürfrechte.
9. Das Spiel wertet das persönliche Ziel aus.

## Choice-IDs in Szene 2

Start:

- `continue:look_around`

Beobachtungen:

- `observe:alena`
- `observe:bastian`
- `observe:runa`
- `observe:caelion`
- `observe:marik`
- `continue:first_talk`

Gespräche:

- `talk:alena`
- `talk:bastian`
- `talk:runa`
- `talk:caelion`
- `talk:marik`

Königspaar:

- `royal:speak`
- `royal:listen`
- `royal:accuse`

Rat:

- `council:hof`
- `council:gilde`
- `council:gesandtschaft`
- `council:balanced`

Ende:

- `continue:ending`

## NPCs

### Herzogin Alena von Falkenruh

Alena steht für Kontrolle und vorsichtige Nutzung der Höhle unter königlicher
Aufsicht. Sie fürchtet Verträge, die der Hof später nicht mehr brechen kann.
Ein Gespräch mit ihr unterstützt die Hofallianz.

### Graf Bastian von Eisenmark

Bastian steht für schnellen Gewinn und sichtbaren Ehrgeiz. Ein Gespräch mit
ihm unterstützt ebenfalls die Hofallianz, aber mit riskanterem Ton. Er merkt
sich, wer ihm widerspricht oder nicht über seine Witze lacht.

### Meisterin Runa Steinhand

Runa steht für Fachwissen, Bergbau und Gildeninteressen. Ein Gespräch mit ihr
unterstützt den Gildenpakt. Ihre Hinweise zeigen, dass die Kristallhöhle auch
körperlich gefährlich ist.

### Lord Caelion Silberblatt

Caelion beobachtet alte Abmachungen und diplomatische Gefahren. Ein Gespräch
mit ihm unterstützt die elfische Gesandtschaft. Für ihn können alte Verträge
zu politischen Waffen werden.

### Hofsekretär Marik Voss

Marik ist offiziell neutral und kennt alte Schriftstücke. Ein Gespräch mit ihm
unterstützt den gemeinsamen Kronenpakt. Seine Mappe enthält Hinweise, die für
mehrere Seiten gefährlich werden können.

### Königin Meridia

Meridia hört eine Stimme aus dem Saal an und prüft, wer Verantwortung statt
nur Gewinn verspricht. Mit `royal:speak` kann der Spieler direkt mit ihr
interagieren.

### König Arwed

Arwed verkündet am Ende, welche Allianz die Schürfrechte erhält.

## Allianzen

Interne Werte:

- `hof`: königliche Hofallianz
- `gilde`: Gildenpakt
- `gesandtschaft`: elfische Gesandtschaft
- `balanced`: gemeinsamer Kronenpakt

Der Rat kann direkt eine Allianz unterstützen. Bei passenden Attributen wird
die gewählte Allianz bestätigt:

- `hof` profitiert von hoher Schlagfertigkeit.
- `gilde` profitiert von hohem Wissen.
- `gesandtschaft` profitiert von hohem Verständnis.
- `balanced` profitiert ebenfalls von hohem Verständnis.

## Story-Flags

`Game` verwendet ein Dictionary `story_flags`.

Gesetztes Flag:

- `first_observed_npc`

Dieses Flag speichert, welche Person der Spieler zuerst beobachtet hat. Es
wird später als Erinnerung ausgewertet, bevor der Spieler ein erstes Gespräch
beginnt und wenn er vor dem Königspaar reagiert.

## Spielende

Nach der Verkündung setzt Szene 2 den Zustand auf fertig. `Game` übernimmt die
Endmeldung aus der Szene und setzt den Gesamtzustand auf `FINISHED`.
Die Endmeldung enthält neben dem Zielstatus einen kurzen persönlichen Text,
der zur Klasse des Spielers passt.

Wichtige Message-ID:

- `game-ballroom-ending`
