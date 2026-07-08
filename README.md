# Python Advanced

Dieses Repository enthält die Aufgabe "Python Advanced" aus dem
Schnupperpraktikum bei RAFISA.

Das Projekt ist ein kleines textbasiertes Rollenspiel mit einer grafischen
Oberfläche in Tkinter. Nach einem kurzen Startbildschirm erstellt der Spieler
eine Figur und betritt danach einen königlichen Ballsaal, in dem über eine neu
entdeckte Höhle und das Schürfrecht verhandelt wird. Die Höhle ist nicht nur
wertvoll, sondern auch politisch gefährlich: Alte Rechte, Gier und
Verantwortung prallen an einem Abend aufeinander.

## Start

Voraussetzung:

- Python 3.10 oder neuer
- keine zusätzlichen Pakete

Spiel starten:

```cmd
python main.py
```

`main.py` erstellt ein `Game`-Objekt, übergibt es an die Tkinter-Oberfläche
und startet die Anwendung mit `Ui.run()`. Im Fenster beginnt das Spiel über
den Button `Start`. Der Button `Stop` schließt das Fenster.

## Aktueller Spielstand

Der aktuelle Code enthält drei Abschnitte:

1. Startbildschirm
2. Charaktererstellung
3. Ballabend mit Beobachtungen, Gesprächen, Ratsentscheidung und Ende

Der Startbildschirm wird beim Laden des Spiels angezeigt. Über `Start` beginnt
die Charaktererstellung. Dort gibt der Spieler einen Namen ein, wählt eine von
drei Klassen, wählt eine von drei Spezies und entscheidet sich für eine
Attributverteilung. Danach beginnt die erste Handlungsszene im Ballsaal.

Im Ballsaal kann der Spieler wichtige Personen beobachten, ein wichtiges
Gespräch führen, vor dem Königspaar reagieren und im Rat eine Allianz
unterstützen. Am Ende des Abends wird verkündet, wer die Schürfrechte erhält.
Erst dann erfährt der Spieler, ob das persönliche Ziel erreicht wurde.
Die erste Beobachtung wird später noch einmal aufgegriffen, damit frühe
Hinweise erzählerisch spürbar bleiben.

## Umgesetzte Anforderungen

- textbasiertes Rollenspiel
- Tkinter-Fenster
- Startbildschirm mit Start- und Stop-Button
- Textausgabe mit Verlauf
- Eingabefeld für Texteingaben
- klickbare Auswahlmöglichkeiten
- Charakteranzeige mit Name, Titel, Spezies, Klasse, Attributen und Ziel
- Charaktererstellung mit Name, 3 Klassen und 3 Spezies
- unterschiedliche Boni durch Spezies
- einfache Handlung am königlichen Hof
- Entscheidungen durch den Spieler
- längere Ballsaalhandlung mit mehreren Plotpunkten
- zielabhängige Erfolgsbedingungen für Aufsteiger, Intrigant und Netzwerker
- Zielstatus in der rechten Sidebar
- klares Ende mit Auswertung
- einfache Fehlerbehandlung bei leeren oder ungültigen Eingaben
- Szeneninhalte werden aus festen `.txt`-Dateien geladen

## Klassen, Spezies und Attribute

Klassen und Ziele:

- Aufsteiger: will, dass die eigene Spezies Teil der Allianz mit
  Schürfrechten wird.
- Intrigant: will verhindern, dass der Rivale Teil der entscheidenden Allianz
  bleibt.
- Netzwerker: will eine neue Verbindung nutzen, um mit einer Person des
  Königspaars zu interagieren.

Spezies:

- Mensch
- Elf
- Zwerg

Im Code und in der Oberfläche wird der Begriff `Spezies` verwendet. Er erfüllt
die Auswahl aus der Aufgabenstellung und passt besser zur Fantasy-Welt des
Spiels.

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
│   └── Scenes/          konkrete Szenen mit Textdateien
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

- `scene0`: Startbildschirm
- `scene1`: Charaktererstellung
- `scene2`: Ballabend und Entscheidung über die Schürfrechte

Jeder Szenenordner enthält einen Unterordner `texts/`. Allgemeine Texte einer
Szene stehen in `system.txt`. NPC-nahe Texte stehen in eigenen Dateien wie
`alena.txt` oder `runa.txt`. Die Dateien werden nicht automatisch gesucht:
Pfade und benötigte Text-Keys sind im jeweiligen Szenenmodul fest eingetragen.

Die GUI sendet Eingaben als `UiResponse` an das Spiel. Das Spiel antwortet mit
einer `GameResponse`. Diese Antwort enthält den Text, den Eingabemodus,
mögliche Auswahloptionen und die aktuellen Charakterdaten.

## Textdateien

Die Textdateien verwenden ein einfaches Blockformat:

```text
[key]
Text über mehrere Zeilen.
```

Der Loader in `src/Utils.py` liest UTF-8, prüft doppelte oder fehlende Keys und
bricht bei ungültigen Dateien mit klaren Fehlermeldungen ab. Platzhalter wie
`{name}` werden im Code mit festen Werten gefüllt. Die Textdateien enthalten
nur angezeigten Inhalt, keine Spiellogik.

## Dokumentation

Die wichtigsten Spielinhalte sind zusätzlich unter `docs/gamecontent/`
dokumentiert. Dort stehen die Begriffe, Szenen, NPCs und Choice-IDs, die im
Code verwendet werden.

## Spielende

Das Spiel endet nach der Verkündung der Schürfrechte. Die rechte Sidebar zeigt
während des Abends Zwischenstände zum persönlichen Ziel. Gewonnen oder verloren
wird aber erst am Ende.
