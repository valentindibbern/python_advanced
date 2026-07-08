# Szene 1: Charaktererstellung

Diese Datei beschreibt den aktuellen Stand der Charaktererstellung im Code.
Die konkrete Szene liegt in `src/Scenes/scene1/scene.py`.

## Zweck

Die Charaktererstellung sammelt alle Daten, die der Spieler vor der ersten
Handlungsszene braucht:

- Name
- Klasse
- Spezies
- Attributverteilung

Die Szene enthält noch keine eigentliche Handlung im Ballsaal, bindet die
Auswahl aber bereits erzählerisch ein. Der Spieler erfährt, welches persönliche
Ziel die Figur verfolgt und warum Spezies und Attribute im höfischen Machtspiel
wichtig sind.

## Ablauf

1. `Game.start_game()` startet die Charaktererstellung.
2. Die Szene fragt nach dem Namen.
3. Ein leerer Name wird abgelehnt.
4. Nach einem gültigen Namen folgt die Klassenauswahl mit Motivation.
5. Nach der Klasse folgt die Speziesauswahl mit politischer Spannung.
6. Nach der Spezies folgt die Attributverteilung mit kurzer Erklärung.
7. Die Szene setzt den Schritt auf `DONE`.
8. `Game` übernimmt den fertigen `Player` und startet Szene 2.

## Schritte im Code

Enum: `CharacterCreationStep`

| Schritt | Bedeutung |
| --- | --- |
| `NAME` | Name per Texteingabe |
| `PLAYER_CLASS` | Klasse per Choice |
| `SPECIES` | Spezies per Choice |
| `ATTRIBUTES` | Attributverteilung per Choice |
| `DONE` | Charakter ist fertig |

## Klassen

Die auswählbaren Klassen kommen aus `Class`:

- Aufsteiger: Der eigene Name soll am Hof mehr Gewicht bekommen.
- Intrigant: Ein Rivale soll geschwächt werden.
- Netzwerker: Ein richtiger Kontakt soll Türen öffnen.

Die Klasse wird gespeichert und bestimmt das persönliche Ziel. Sie gibt keinen
Attributbonus.

## Spezies

Die auswählbaren Spezies kommen aus `Species`:

- Mensch
- Elf
- Zwerg

Die Spezies gibt einen Attributbonus:

- Mensch: +1 Schlagfertigkeit
- Elf: +1 Verständnis
- Zwerg: +1 Wissen

Die Auswahltexte zeigen zusätzlich die erzählerische Rolle:

- Menschen sind nahe am Hof, aber in Absprachen verstrickt.
- Elfen bringen alte Rechte mit, denen der Hof misstraut.
- Zwerge kennen die Tiefe, werden aber leicht als Werkzeug behandelt.

## Attributverteilung

Der Spieler wählt ein Hauptattribut:

- Wissen
- Schlagfertigkeit
- Verständnis

Vor der Auswahl erklärt die Szene kurz, wofür die Attribute in Gesprächen,
Urkunden und politischen Situationen stehen.

Das Hauptattribut erhält 2 Punkte. Die beiden anderen Attribute erhalten je
1 Punkt. Danach wird der Speziesbonus addiert.

## Schnittstelle zu Game

Die Szene gibt immer eine `GameResponse` zurück. Diese enthält:

- Text für die UI
- Eingabemodus
- mögliche Auswahloptionen
- aktuelle Charakterdaten

Wenn die Szene fertig ist, fragt `Game` über `get_player()` den fertigen
Spieler ab und speichert ihn in `Game.player`.

## Schnittstelle zur UI

Die UI verarbeitet keine Spiellogik. Sie zeigt nur die Antwort von `Game` an
und sendet Texteingaben oder Choice-IDs zurück.

Wichtige UI-Modi:

- `InputMode.TEXT` für den Namen
- `InputMode.CHOICE` für Klasse, Spezies und Attribute
- `InputMode.NONE` nach Abschluss der Szene
