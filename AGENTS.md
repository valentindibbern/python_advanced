# AGENTS.md

Diese Datei beschreibt, wie in diesem Projekt gearbeitet werden soll.
Sie gilt für alle Dateien im Repository.

## Projektziel

Dieses Repository enthält die Aufgabe "Python Advanced" aus dem
Schnupperpraktikum bei RAFISA.

Ziel ist ein kleines textbasiertes Rollenspiel mit Python und Tkinter.
Das Spiel soll einfach, verständlich und lauffähig sein. Es muss nicht
groß oder komplex sein, soll aber die Anforderungen aus der Aufgabenstellung
sauber erfüllen.

## Wichtigste Anforderungen

Das Spiel soll folgende Punkte enthalten:

- ein textbasiertes Rollenspiel
- eine grafische Oberfläche mit Tkinter
- eine Darstellung des Spieltexts im Fenster
- ein Eingabefeld für Text
- eine Charaktererstellung
- Eingabe eines Namens
- Auswahl aus 3 Klassen
- Auswahl aus 3 Rassen
- unterschiedliche Boni je nach Klasse und Rasse
- eine einfache Handlung
- Entscheidungen durch den Spieler
- ein klares Ende

Beispiele für Boni:

- Ein Krieger hat mehr Stärke als ein Magier.
- Ein Elf hat mehr Geschick als ein Mensch.

## Technische Regeln

- Verwende keine Third-Party-Dependencies.
- Verwende nur Python-Standardbibliothek.
- Verwende Tkinter für die GUI.
- Halte den Code so einfach wie möglich.
- Schreibe Code so, dass ihn ein Python-Anfänger erklären kann.
- Vermeide unnötige Abstraktionen.
- Vermeide komplexe Frameworks, Patterns oder Metaprogrammierung.
- Keine externen Assets einbauen, wenn sie nicht wirklich gebraucht werden.
- Keine Netzwerkzugriffe für das Spiel.

## Python-Version

Das Projekt soll mit einer normalen lokalen Python-Version lauffähig sein.
Wenn möglich, schreibe Code kompatibel mit Python 3.10 oder neuer.

Keine Syntax verwenden, die nur in sehr neuen Python-Versionen funktioniert,
wenn sie nicht nötig ist.

## Projektstruktur

Bevorzugte Struktur:

```text
python_advanced/
├── docs/        Aufgabenstellung, Unterlagen und Spielinhalte
│   └── gamecontent/ Register für Figuren, Szenen und Beschreibungen
├── src/         Quellcode des Spiels
├── main.py      Startpunkt des Programms
├── README.md    Projektbeschreibung
└── AGENTS.md    Arbeitsregeln für dieses Projekt
```

`main.py` soll der einfache Startpunkt bleiben. Wenn der eigentliche Code in
`src` liegt, soll `main.py` nur importieren und starten.

## Code-Stil

- Verwende sprechende Namen.
- Schreibe kurze Funktionen.
- Eine Funktion soll möglichst nur eine klare Aufgabe haben.
- Nutze einfache Datentypen wie `dict`, `list`, `str`, `int` und `bool`.
- Verwende Klassen nur, wenn sie den Code wirklich einfacher machen.
- Halte Spiellogik und GUI möglichst getrennt.
- Schreibe keine überlangen Dateien, wenn eine einfache Aufteilung hilft.
- Kommentare nur dort schreiben, wo sie beim Verstehen helfen.
- Verwende Typehinting für Funktionen, Methoden, Variablen und Datenstrukturen.
- Typehints sollen präzise sein, auch für verschachtelte Listen,
  Dictionaries und Objekte. Nicht nur die erste Ebene typisieren.
- Verwende deutsche Umlaute wie `ä`, `ö` und `ü` direkt im Code, in Texten und
  in der Dokumentation.
- Falls Umlaute an einer Stelle technisch unmöglich sind, schreibe dort einen
  kurzen `TODO`-Kommentar mit der Begründung.

Guter Stil für dieses Projekt bedeutet nicht, möglichst professionell oder
kompliziert zu wirken. Guter Stil bedeutet hier: klar, direkt, erklärbar.

## GUI-Regeln

Die GUI soll mit Tkinter umgesetzt werden.

Die Oberfläche soll mindestens enthalten:

- ein Textfeld oder Label für die Geschichte und Rückmeldungen
- ein Eingabefeld für Spielerantworten
- einen Button zum Absenden

Optional sind weitere einfache Elemente erlaubt:

- Buttons für Auswahlmöglichkeiten
- Labels für Charakterwerte
- ein Start- oder Neustart-Button

Die GUI soll funktional und übersichtlich sein. Aufwendiges Styling ist nicht
wichtig.

## Spiellogik

Die Spiellogik soll einfach nachvollziehbar sein.

Empfohlener Aufbau:

- Charakter erstellen
- Startszene anzeigen
- Spieler trifft Entscheidungen
- Werte beeinflussen einzelne Situationen
- Spiel endet mit Gewinn oder Verlust

Das Spiel darf kurz sein. Wichtiger ist, dass es vollständig funktioniert.

## Charakterwerte

Mögliche Werte:

- Stärke
- Geschick
- Magie
- Leben

Es müssen nicht alle diese Werte verwendet werden. Wenn Werte verwendet
werden, sollen sie eine erkennbare Bedeutung im Spiel haben.

## Fehlerbehandlung

Das Spiel soll falsche Eingaben freundlich behandeln.

Beispiele:

- leere Eingaben nicht ungeprüft akzeptieren
- unbekannte Befehle mit einem Hinweis beantworten
- bei Auswahlfragen klar sagen, welche Eingaben erlaubt sind

Fehlerbehandlung soll einfach bleiben. Keine komplizierten Validierungs-Systeme.

## Tests und Prüfung

Vor Abschluss einer Änderung soll geprüft werden:

- Startet das Spiel mit `python main.py`?
- Öffnet sich das Tkinter-Fenster?
- Kann ein Charakter erstellt werden?
- Führt das Spiel bis zu einem Ende?
- Gibt es keine offensichtlichen Abstürze bei falschen Eingaben?

Automatisierte Tests sind optional. Wenn Tests geschrieben werden, nur mit
Standardbibliothek, zum Beispiel `unittest`.

## Dokumentation

README.md soll kurz erklären:

- was das Projekt ist
- wie man das Spiel startet
- welche Anforderungen umgesetzt wurden

Keine lange Dokumentation schreiben, wenn sie dem Projekt nicht hilft.

Unter `docs/gamecontent/` soll ein ausführliches Register für alle
Spielinhalte entstehen. Dort sollen NPCs, Szenen, Beschreibungen, Orte,
Entscheidungen, Dialoge und wichtige Begriffe festgehalten werden, damit sie im
Code, in der Dokumentation und im Spieltext überall übereinstimmen.

## Git-Hinweise

- Keine generierten Dateien committen, wenn sie nicht gebraucht werden.
- Keine `.venv`, IDE-Dateien oder temporäre Render-Dateien committen.
- Änderungen klein und nachvollziehbar halten.
- Nach jeder erledigten Aufgabe soll ein Commit erstellt werden.
- Die Commit-Beschreibung soll klar beschreiben, was implementiert wurde.

## Wichtige Einschränkungen

- Nicht versuchen, ein großes RPG-System zu bauen.
- Nicht zu viele Features auf einmal einbauen.
- Nicht die Aufgabenstellung überkomplizieren.
- Nicht ohne Grund Dependencies hinzufügen.
- Nicht den Fokus auf Tkinter und lauffähige Spiellogik verlieren.

Wenn es mehrere mögliche Lösungen gibt, wähle die einfachste Lösung, die die
Anforderung sauber erfüllt.
