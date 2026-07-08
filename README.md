# Python Advanced

Dieses Repository enthält die Aufgabe "Python Advanced" aus dem
Schnupperpraktikum bei RAFISA.

Das Projekt ist ein kleines textbasiertes Rollenspiel mit einer grafischen
Oberfläche in Tkinter. Der Spieler erstellt zuerst eine Figur und betritt
danach einen königlichen Ballsaal, in dem über eine neu entdeckte Höhle und
das Schürfrecht verhandelt wird.

## Start

Voraussetzung:

- Python 3.10 oder neuer
- keine zusätzlichen Pakete

Spiel starten:

```cmd
python main.py
```

`main.py` erstellt ein `Game`-Objekt, übergibt es an die Tkinter-Oberfläche
und startet die Anwendung mit `Ui.run()`.

## Aktueller Spielstand

Der aktuelle Code enthält zwei Abschnitte:

1. Charaktererstellung
2. Ankunft im Ballsaal

In der Charaktererstellung gibt der Spieler einen Namen ein, wählt eine von
drei Klassen, wählt eine von drei Spezies und entscheidet sich für eine
Attributverteilung. Danach beginnt die erste Handlungsszene im Ballsaal.

Im Ballsaal kann der Spieler wichtige Personen beobachten. Dabei werden
Informationen über ihre Ziele, Interessen und mögliche Konflikte gesammelt.
Wenn alle wichtigen Personen beobachtet wurden, ist die Ballsaal-Szene fertig.
Eine dritte Szene ist im aktuellen Code noch nicht vorhanden.

## Umgesetzte Anforderungen

- textbasiertes Rollenspiel
- Tkinter-Fenster
- Textausgabe mit Verlauf
- Eingabefeld für Texteingaben
- klickbare Auswahlmöglichkeiten
- Charakteranzeige mit Name, Titel, Spezies, Klasse, Attributen und Ziel
- Charaktererstellung mit Name, 3 Klassen und 3 Spezies
- unterschiedliche Boni durch Spezies
- einfache Handlung am königlichen Hof
- Entscheidungen durch den Spieler
- Abschluss der aktuellen Ballsaal-Szene
- einfache Fehlerbehandlung bei leeren oder ungültigen Eingaben

## Klassen, Spezies und Attribute

Klassen:

- Aufsteiger
- Intrigant
- Netzwerker

Spezies:

- Mensch
- Elf
- Zwerg

Attribute:

- Wissen
- Schlagfertigkeit
- Verständnis

Die Attributverteilung nutzt das Muster `2, 1, 1`. Der Spieler wählt ein
Hauptattribut, das 2 Punkte erhält. Die anderen beiden Attribute erhalten je
1 Punkt. Danach gibt die Spezies einen zusätzlichen Bonus:

- Mensch: +1 Schlagfertigkeit
- Elf: +1 Verständnis
- Zwerg: +1 Wissen

## Projektstruktur

```text
python_advanced/
├── docs/
│   ├── gamecontent/     Register für Spielinhalte
│   ├── gescannt/        gescannte Aufgabenunterlagen
│   ├── ideen/           frühe Ideen und Mindmaps
│   ├── pläne/           Planungsnotizen
│   └── spielkonzept.md  Konzept und aktueller Spielinhalt
├── src/
│   ├── Classes/         Game, UI, Player und Szenen-Basisklasse
│   ├── Datatypes/       Enums und TypedDict-Modelle
│   └── Scenes/          konkrete Szenen
├── main.py              Startpunkt
├── pyproject.toml       Projektmetadaten
└── README.md
```

## Aufbau im Code

Die Spiellogik liegt in `src/Classes/Game.py`. `Game` hält den aktuellen
Spielzustand, den Spieler, die aktuelle Szene und Story-Flags.

Die Oberfläche liegt in `src/Classes/Ui.py`. Sie zeigt die Geschichte, die
Charakterdaten, ein Texteingabefeld und Auswahlmöglichkeiten an.

Die konkreten Szenen liegen unter `src/Scenes/`:

- `scene1`: Charaktererstellung
- `scene2`: Ankunft im Ballsaal

Die GUI sendet Eingaben als `UiResponse` an das Spiel. Das Spiel antwortet mit
einer `GameResponse`. Diese Antwort enthält den Text, den Eingabemodus,
mögliche Auswahloptionen und die aktuellen Charakterdaten.

## Dokumentation

Die wichtigsten Spielinhalte sind zusätzlich unter `docs/gamecontent/`
dokumentiert. Dort stehen die Begriffe, Szenen, NPCs und Choice-IDs, die im
Code verwendet werden.

## Bekannte Grenze

Nach der Ballsaal-Szene gibt es noch keine weitere Szene. Der Code versucht
danach aktuell, eine Szene mit ID `2` zu laden. Bis eine dritte Szene oder eine
saubere Ende-Behandlung ergänzt ist, ist dieser Punkt die technische Grenze des
Spielverlaufs.
