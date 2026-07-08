# Spielinhaltsregister

Dieses Register beschreibt die Begriffe, Szenen, Figuren und Choice-IDs, die
im aktuellen Code verwendet werden.

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
- Erfolg, wenn der Spieler vor dem Königspaar `royal:speak` wählt.

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

- Begrüßt den Spieler beim Laden des Fensters.
- Erklärt den Start über den Button `Start`.
- Verweist darauf, dass `Stop` das Fenster schließt.

Wichtige Message-ID:

- `game-start-screen`

## Szene 1: Charaktererstellung

Code-Datei: `src/Scenes/scene1/scene.py`

Titel in der UI: `Charaktererstellung`

Ablauf:

1. Name eingeben
2. Klasse wählen
3. Spezies wählen
4. Attributverteilung wählen
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
4. Der Spieler reagiert auf den Auftritt des Königspaars.
5. Der Spieler unterstützt im Rat eine Allianz.
6. Das Königspaar verkündet die Schürfrechte.
7. Das Spiel wertet das persönliche Ziel aus.

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
Aufsicht. Ein Gespräch mit ihr unterstützt die Hofallianz.

### Graf Bastian von Eisenmark

Bastian steht für schnellen Gewinn und sichtbaren Ehrgeiz. Ein Gespräch mit
ihm unterstützt ebenfalls die Hofallianz, aber mit riskanterem Ton.

### Meisterin Runa Steinhand

Runa steht für Fachwissen, Bergbau und Gildeninteressen. Ein Gespräch mit ihr
unterstützt den Gildenpakt.

### Lord Caelion Silberblatt

Caelion beobachtet alte Abmachungen und diplomatische Gefahren. Ein Gespräch
mit ihm unterstützt die elfische Gesandtschaft.

### Hofsekretär Marik Voss

Marik ist offiziell neutral und kennt alte Schriftstücke. Ein Gespräch mit ihm
unterstützt den gemeinsamen Kronenpakt.

### Königin Meridia

Meridia hört eine Stimme aus dem Saal an. Mit `royal:speak` kann der Spieler
direkt mit ihr interagieren.

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
wird aktuell gespeichert, aber noch nicht für weitere Szenen ausgewertet.

## Spielende

Nach der Verkündung setzt Szene 2 den Zustand auf fertig. `Game` übernimmt die
Endmeldung aus der Szene und setzt den Gesamtzustand auf `FINISHED`.

Wichtige Message-ID:

- `game-ballroom-ending`
