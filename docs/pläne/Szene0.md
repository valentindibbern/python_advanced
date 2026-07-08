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

Die Szene enthält noch keine eigentliche Handlung. Sie bereitet den `Player`
für die folgenden Szenen vor.

## Ablauf

1. `Game.start()` startet die erste Szene.
2. Die Szene fragt nach dem Namen.
3. Ein leerer Name wird abgelehnt.
4. Nach einem gültigen Namen folgt die Klassenauswahl.
5. Nach der Klasse folgt die Speziesauswahl.
6. Nach der Spezies folgt die Attributverteilung.
7. Die Szene setzt den Schritt auf `DONE`.
8. `Game` übernimmt den fertigen `Player` und startet die nächste Szene.

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

- Aufsteiger
- Intrigant
- Netzwerker

Die Klasse wird aktuell gespeichert, gibt aber noch keinen Attributbonus.

## Spezies

Die auswählbaren Spezies kommen aus `Species`:

- Mensch
- Elf
- Zwerg

Die Spezies gibt einen Attributbonus:

- Mensch: +1 Schlagfertigkeit
- Elf: +1 Verständnis
- Zwerg: +1 Wissen

## Attributverteilung

Der Spieler wählt ein Hauptattribut:

- Wissen
- Schlagfertigkeit
- Verständnis

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
