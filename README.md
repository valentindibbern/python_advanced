# Python Advanced

Dieses Repository enthält die zweite Python-Aufgabe aus dem Schnupperpraktikum bei RAFISA.

Ziel ist ein kleines textbasiertes Rollenspiel mit Python und Tkinter. Das Spiel soll einfach aufgebaut sein, aber die wichtigsten Anforderungen aus der Aufgabenstellung erfüllen.

## Aufgabe

Das Spiel ist ein Rollenspiel mit Charaktererstellung, einer einfachen Handlung und einem klaren Ende.

Der Spieler soll zu Beginn einen Charakter erstellen:

- Name eingeben
- eine von 3 Klassen auswählen
- eine von 3 Rassen auswählen
- je nach Klasse und Rasse unterschiedliche Werte oder Boni erhalten

Beispiel:

- Ein Krieger hat mehr Stärke als ein Magier.
- Ein Elf hat mehr Geschick als ein Mensch.

Danach soll der Spieler Entscheidungen treffen können, die den Verlauf des Spiels beeinflussen.

## Anforderungen

- Python 3.10 oder neuer
- keine Third-Party-Dependencies
- Tkinter für die grafische Oberfläche
- Darstellung des Spiels in einem GUI-Fenster
- Eingabefeld für Text
- lauffähiges Spiel mit Ende

## Installation

Repository klonen:

```cmd
git clone https://github.com/valentindibbern/python_advanced.git
cd python_advanced
```

Spiel starten:

```cmd
python main.py
```

## Projektstruktur

```text
python_advanced/
├── docs/        Aufgabenstellung
├── src/         Quellcode des Spiels
├── main.py      Startpunkt des Programms
└── README.md    Projektbeschreibung
```

## Aufbau im Code

`main.py` erstellt das Spiel und die Tkinter-Oberfläche. Die Oberfläche startet
mit `Ui.run()` die `mainloop()`.

Die UI sendet Eingaben als `UiResponse` an das Spiel. Das Spiel kennt keine
Tkinter-Elemente und antwortet mit einer `GameResponse`. Diese Antwort enthält
den Spieltext, den Eingabemodus, mögliche Auswahloptionen und die aktuellen
Charakterdaten.

## Hinweise

Der Code soll möglichst einfach und verständlich bleiben. Es werden keine externen Pakete verwendet.
