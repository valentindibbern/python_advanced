# Plan: Scene 0 fuer Charaktererstellung und Szenenstruktur

## Zusammenfassung

Es wird eine einfache Szenenstruktur vorbereitet, bei der jede Szene in einem eigenen Ordner liegt. Szene `0` ist die Charaktererstellung und enthaelt keine Rollenspielhandlung, sondern nur den technischen Ablauf:

1. Name eingeben
2. Klasse aus vorhandener `Class`-Enum waehlen
3. Spezies aus vorhandener `Species`-Enum waehlen
4. `PC` erstellen und dauerhaft in `Game.player` speichern
5. Charakterdaten an die UI zurueckgeben
6. Danach bereit fuer die naechste Szene sein

Der Informationsfluss zwischen Szenen laeuft nicht ueber Dateien, sondern ueber das `Game`-Objekt. Persistente Spieldaten wie `player`, `state`, `current_scene_id` und spaeter weitere Flags bleiben in `Game`.

## Szenenstruktur

Im Projektroot wird der vorhandene bzw. neue Ordner `Scenes` genutzt:

```text
Scenes/
└── 0/
    ├── scene.py
    └── npcs/
```

Fuer Szene `0` bleibt `npcs/` leer, weil die Charaktererstellung keine NPCs braucht.

`../../src/Scenes/0/scene.py` enthaelt eine Klasse fuer den Ablauf der Charaktererstellung, z.B. `CharacterCreationScene`. Diese Klasse enthaelt keine Tkinter-Logik und keine Story-Elemente.

Die Szene speichert nur ihren eigenen Fortschritt:

```python
self.step
self.name
self.player_class
self.species
```

Die fertige Figur wird am Ende an `Game` zurueckgegeben oder direkt ueber eine Methode an `Game.player` uebergeben.

## Game-Integration

`Game.start()` soll nicht mehr den Platzhaltertext anzeigen, sondern Szene `0` laden und starten.

Neue oder angepasste Felder in `Game`:

```python
self.state: State
self.player: PC | None
self.current_scene: CharacterCreationScene | None
self.current_scene_id: str
```

Ablauf:

- `Game.__init__()` setzt `current_scene_id = "0"` und `player = None`
- `Game.start()` erstellt `CharacterCreationScene()`
- `Game.start()` ruft `self.current_scene.start()` auf
- `Game.handle_text_input(text)` leitet Texteingaben an die aktuelle Szene weiter
- `Game.handle_choice(choice_id)` leitet Choices an die aktuelle Szene weiter
- Wenn Szene `0` fertig ist, speichert `Game` den erzeugten `PC` in `self.player`

Die UI bleibt unveraendert in ihrer Rolle: Sie ruft nur `Game.start()`, `Game.handle_text_input(...)` und `Game.handle_choice(...)` auf.

## Scene-0-Ablauf

Szene `0` nutzt die bestehende UI-Schnittstelle mit `InputMode.TEXT` und `InputMode.CHOICE`.

### Schritt 1: Name

Startantwort:

```python
text = "Wie heisst dein Charakter?"
input_mode = InputMode.TEXT
choices = []
character = None
is_finished = False
```

Bei leerem Namen:

```python
text = "Bitte gib einen Namen ein."
input_mode = InputMode.TEXT
```

Bei gueltigem Namen:

- Name wird in der Szene gespeichert
- Szene wechselt zu Klassenauswahl

### Schritt 2: Klasse

Choices werden aus der vorhandenen `Class`-Enum erzeugt:

```python
[
    {"id": "class:ASPIRANT", "label": "Aspirant"},
    {"id": "class:INTRIGANT", "label": "Intrigant"},
    {"id": "class:NETZWERKER", "label": "Netzwerker"},
]
```

Bei gueltiger Wahl:

- `self.player_class` wird gesetzt
- Szene wechselt zu Speziesauswahl

Bei ungueltiger Choice-ID:

- Szene bleibt bei Klassenauswahl
- GameResponse erklaert, dass die Auswahl ungueltig ist

### Schritt 3: Spezies

Choices werden aus der vorhandenen `Species`-Enum erzeugt:

```python
[
    {"id": "species:HUMAN", "label": "Mensch"},
    {"id": "species:ELF", "label": "Elf"},
    {"id": "species:DWARF", "label": "Zwerg"},
]
```

Bei gueltiger Wahl:

- `self.species` wird gesetzt
- `PC` wird erstellt
- `Game.player` wird dauerhaft gesetzt
- Charakterdaten werden an die UI geliefert

Szene `0` endet danach technisch mit:

```python
input_mode = InputMode.NONE
is_finished = False
```

`is_finished` bleibt `False`, weil nur die Charaktererstellung fertig ist, nicht das ganze Spiel.

## Interfaces und Typen

Die vorhandene Response-Struktur bleibt bestehen:

```python
GameResponse:
    text: str
    input_mode: InputMode
    choices: list[Choice]
    character: CharacterData | None
    is_finished: bool
```

Ergaenzung fuer Szenen:

```python
class SceneResult(TypedDict, total=False):
    response: GameResponse
    player: PC
    next_scene_id: str
```

Alternativ kann Szene `0` direkt eine `GameResponse` liefern und `Game` fragt nach Abschluss `scene.create_player()` ab. Die empfohlene einfachere Variante ist:

- Szene verarbeitet Eingabe
- Szene gibt `GameResponse` zurueck
- Szene stellt fertigen Spieler ueber `get_player()` bereit
- `Game` speichert ihn in `self.player`

Damit bleibt der Informationsfluss klar: Szenen erzeugen Daten, aber `Game` besitzt die dauerhaften Daten.

## Wichtige Code-Anpassungen

- Import-Pfade vereinheitlichen: `Ui.py` soll `InputMode` konsistent ueber `src.Enums.InputMode` importieren, nicht ueber `Enums.InputMode`.
- `Game` bekommt eine kleine Ladefunktion fuer Szene `0`, z.B. `_load_scene(scene_id: str)`.
- `Game` kennt fuer jetzt nur `"0"`; weitere Szenen koennen spaeter in derselben Funktion ergaenzt werden.
- `../../src/Scenes/0/scene.py` importiert `PC`, `Class`, `Species`, `InputMode` und die Response-Typen.
- `Scene.py` in `src/Classes` bleibt als allgemeiner einfacher Datencontainer bestehen; die konkrete Szene `0` darf eine eigene Ablaufklasse haben.
- Keine NPC-Dateien fuer Szene `0`, weil diese Szene ausdruecklich keine Rollenspiel-Elemente enthalten soll.

## Testplan

Manuell oder per kurzem Python-Flow pruefen:

- `Game.start()` fragt nach dem Namen.
- Leerer Name bleibt im Textmodus und erzeugt eine Fehlermeldung.
- Gueltiger Name zeigt Klassenauswahl.
- Ungueltige Choice-ID bleibt bei der aktuellen Auswahl.
- Gueltige Klasse zeigt Speziesauswahl.
- Gueltige Spezies erstellt `Game.player`.
- `Game.player.name`, `Game.player.player_class` und `Game.player.species` sind korrekt gesetzt.
- `GameResponse["character"]` zeigt Name, Klasse und Spezies in der UI.
- Tkinter-Flow funktioniert: Name eingeben, Klasse klicken, Spezies klicken.
- `python main.py` startet weiterhin.
- Es werden keine Third-Party-Dependencies eingefuehrt.

## Annahmen

- Szene `0` ist nur Charaktererstellung und enthaelt keine Story, Raeume oder NPC-Dialoge.
- Der Ordner `Scenes` liegt im Projektroot, nicht unter `src`.
- Jede spaetere Szene bekommt ebenfalls einen eigenen Ordner unter `Scenes`.
- Dauerhafte Informationen zwischen Szenen werden in `Game` gespeichert, nicht in Szenendateien.
- `Class`, `Species` und `PC` werden jetzt direkt fuer die Charaktererstellung verwendet.
- Attribute/Boni werden in diesem Schritt noch nicht umgesetzt, weil du nur Name, Klasse usw. fuer die erste technische Szene genannt hast.
