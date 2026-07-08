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

Der Titel ist aktuell immer `Baron`. Das Ziel-Feld ist vorhanden, wird aber
noch nicht automatisch gesetzt.

## Klassen

Code-Enum: `Class`

| Enum-Wert | Anzeige |
| --- | --- |
| `AUFSTEIGER` | Aufsteiger |
| `INTRIGANT` | Intrigant |
| `NETZWERKER` | Netzwerker |
| `NOTSET` | Nicht gesetzt |

Choice-IDs in der Charaktererstellung:

- `class:AUFSTEIGER`
- `class:INTRIGANT`
- `class:NETZWERKER`

## Spezies

Code-Enum: `Species`

| Enum-Wert | Anzeige | Bonus |
| --- | --- | --- |
| `HUMAN` | Mensch | +1 Schlagfertigkeit |
| `ELF` | Elf | +1 Verständnis |
| `DWARF` | Zwerg | +1 Wissen |
| `NOTSET` | Nicht gesetzt | kein Bonus |

Choice-IDs in der Charaktererstellung:

- `species:HUMAN`
- `species:ELF`
- `species:DWARF`

## Attribute

Code-Enum: `Attributes`

| Enum-Wert | Anzeige |
| --- | --- |
| `KNOWLEDGE` | Wissen |
| `WIT` | Schlagfertigkeit |
| `UNDERSTANDING` | Verständnis |

Die Startverteilung nutzt das Muster `2, 1, 1`. Der Spieler wählt ein
Hauptattribut:

- `attributes:KNOWLEDGE`
- `attributes:WIT`
- `attributes:UNDERSTANDING`

Danach wird der Speziesbonus addiert.

## Szene 1: Charaktererstellung

Code-Datei: `src/Scenes/scene1/scene.py`

Titel in der UI: `Charaktererstellung`

Ablauf:

1. Name eingeben
2. Klasse wählen
3. Spezies wählen
4. Attributverteilung wählen
5. Charakter abschließen

Fehlerbehandlung:

- Leerer Name: `Bitte gib einen Namen ein.`
- Falsche Eingabe bei Auswahlfragen: Hinweis auf die angezeigten Optionen
- Ungültige Klasse: `Bitte wähle eine gültige Klasse.`
- Ungültige Spezies: `Bitte wähle eine gültige Spezies.`
- Ungültige Attributverteilung: `Bitte wähle eine gültige Attributverteilung.`

Wichtige Message-IDs:

- `game-character-name-question`
- `game-character-name-error`
- `game-character-class-question`
- `game-character-species-question`
- `game-character-attributes-question`
- `game-character-created`

## Szene 2: Ankunft im Ballsaal

Code-Datei: `src/Scenes/scene2/scene.py`

Titel in der UI:

- `Ankunft im Ballsaal`
- `Ballsaal`

Ablauf:

1. Der Spieler kommt im Ballsaal an.
2. Der Spieler wählt `Dich im Saal umsehen`.
3. Der Spieler beobachtet fünf wichtige Personen.
4. Nachdem alle Personen beobachtet wurden, wählt der Spieler
   `Dich unter die Gäste mischen`.
5. Die Ballsaal-Szene ist fertig.

Choice-IDs:

- `continue:look_around`
- `npc:duchess`
- `npc:count`
- `npc:guildmaster`
- `npc:envoy`
- `npc:secretary`
- `continue:end_scene`

Wichtige Message-IDs:

- `game-ballroom-arrival`
- `game-ballroom-npc-overview`
- `game-ballroom-observation`
- `game-ballroom-all-observed`
- `game-ballroom-finished`

## NPCs

### Herzogin Alena von Falkenruh

Choice-ID: `npc:duchess`

Story-Flag-Wert bei erster Beobachtung: `duchess`

Alena steht für Kontrolle und vorsichtige Nutzung der Höhle unter königlicher
Aufsicht. Sie will verhindern, dass ein einzelnes Haus zu mächtig wird.

### Graf Bastian von Eisenmark

Choice-ID: `npc:count`

Story-Flag-Wert bei erster Beobachtung: `count`

Bastian steht für schnellen Gewinn, Arbeit und Ehrgeiz. Seine Versprechen
wirken attraktiv, machen andere aber abhängig von seiner Macht.

### Meisterin Runa Steinhand

Choice-ID: `npc:guildmaster`

Story-Flag-Wert bei erster Beobachtung: `guildmaster`

Runa steht für Bergbau, Handwerk und Gildeninteressen. Sie denkt praktisch und
warnt vor hastiger Ausbeutung.

### Lord Caelion Silberblatt

Choice-ID: `npc:envoy`

Story-Flag-Wert bei erster Beobachtung: `envoy`

Caelion sucht nach verborgener Angst, alten Abmachungen und diplomatischen
Gefahren.

### Hofsekretär Marik Voss

Choice-ID: `npc:secretary`

Story-Flag-Wert bei erster Beobachtung: `secretary`

Marik ist offiziell neutral. Er kennt vermutlich Schriftstücke, Ansprüche und
alte Abmachungen, die für die Höhle wichtig sind.

## Story-Flags

Aktuell verwendet `Game` ein Dictionary `story_flags`.

Gesetztes Flag:

- `first_observed_npc`

Dieses Flag speichert, welche Person der Spieler im Ballsaal zuerst beobachtet
hat. Es wird im aktuellen Code noch nicht weiter ausgewertet.

## Aktuelle Grenze

Nach der Ballsaal-Szene gibt es noch keine weitere spielbare Szene. Der Code
versucht danach aktuell, Szene ID `2` zu laden. Diese Szene existiert noch
nicht.
