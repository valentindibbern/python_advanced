# AGENTS.md

Diese Datei beschreibt, wie in diesem Projekt gearbeitet werden soll.
Sie gilt fuer alle Dateien im Repository.

## Projektziel

Dieses Repository enthaelt die Aufgabe "Python Advanced" aus dem
Schnupperpraktikum bei RAFISA.

Ziel ist ein kleines textbasiertes Rollenspiel mit Python und Tkinter.
Das Spiel soll einfach, verstaendlich und lauffaehig sein. Es muss nicht
gross oder komplex sein, soll aber die Anforderungen aus der Aufgabenstellung
sauber erfuellen.

## Wichtigste Anforderungen

Das Spiel soll folgende Punkte enthalten:

- ein textbasiertes Rollenspiel
- eine grafische Oberflaeche mit Tkinter
- eine Darstellung des Spieltexts im Fenster
- ein Eingabefeld fuer Text
- eine Charaktererstellung
- Eingabe eines Namens
- Auswahl aus 3 Klassen
- Auswahl aus 3 Rassen
- unterschiedliche Boni je nach Klasse und Rasse
- eine einfache Handlung
- Entscheidungen durch den Spieler
- ein klares Ende

Beispiele fuer Boni:

- Ein Krieger hat mehr Staerke als ein Magier.
- Ein Elf hat mehr Geschick als ein Mensch.

## Technische Regeln

- Verwende keine Third-Party-Dependencies.
- Verwende nur Python-Standardbibliothek.
- Verwende Tkinter fuer die GUI.
- Halte den Code so einfach wie moeglich.
- Schreibe Code so, dass ihn ein Python-Anfaenger erklaeren kann.
- Vermeide unnoetige Abstraktionen.
- Vermeide komplexe Frameworks, Patterns oder Metaprogrammierung.
- Keine externen Assets einbauen, wenn sie nicht wirklich gebraucht werden.
- Keine Netzwerkzugriffe fuer das Spiel.

## Python-Version

Das Projekt soll mit einer normalen lokalen Python-Version lauffaehig sein.
Wenn moeglich, schreibe Code kompatibel mit Python 3.10 oder neuer.

Keine Syntax verwenden, die nur in sehr neuen Python-Versionen funktioniert,
wenn sie nicht noetig ist.

## Projektstruktur

Bevorzugte Struktur:

```text
python_advanced/
├── docs/        Aufgabenstellung und Unterlagen
├── src/         Quellcode des Spiels
├── main.py      Startpunkt des Programms
├── README.md    Projektbeschreibung
└── AGENTS.md    Arbeitsregeln fuer dieses Projekt
```

`main.py` soll der einfache Startpunkt bleiben. Wenn der eigentliche Code in
`src` liegt, soll `main.py` nur importieren und starten.

## Code-Stil

- Verwende sprechende Namen.
- Schreibe kurze Funktionen.
- Eine Funktion soll moeglichst nur eine klare Aufgabe haben.
- Nutze einfache Datentypen wie `dict`, `list`, `str`, `int` und `bool`.
- Verwende Klassen nur, wenn sie den Code wirklich einfacher machen.
- Halte Spiellogik und GUI moeglichst getrennt.
- Schreibe keine ueberlangen Dateien, wenn eine einfache Aufteilung hilft.
- Kommentare nur dort schreiben, wo sie beim Verstehen helfen.

Guter Stil fuer dieses Projekt bedeutet nicht, moeglichst professionell oder
kompliziert zu wirken. Guter Stil bedeutet hier: klar, direkt, erklaerbar.

## GUI-Regeln

Die GUI soll mit Tkinter umgesetzt werden.

Die Oberflaeche soll mindestens enthalten:

- ein Textfeld oder Label fuer die Geschichte und Rueckmeldungen
- ein Eingabefeld fuer Spielerantworten
- einen Button zum Absenden

Optional sind weitere einfache Elemente erlaubt:

- Buttons fuer Auswahlmoeglichkeiten
- Labels fuer Charakterwerte
- ein Start- oder Neustart-Button

Die GUI soll funktional und uebersichtlich sein. Aufwendiges Styling ist nicht
wichtig.

## Spiellogik

Die Spiellogik soll einfach nachvollziehbar sein.

Empfohlener Aufbau:

- Charakter erstellen
- Startszene anzeigen
- Spieler trifft Entscheidungen
- Werte beeinflussen einzelne Situationen
- Spiel endet mit Gewinn oder Verlust

Das Spiel darf kurz sein. Wichtiger ist, dass es vollstaendig funktioniert.

## Charakterwerte

Moegliche Werte:

- Staerke
- Geschick
- Magie
- Leben

Es muessen nicht alle diese Werte verwendet werden. Wenn Werte verwendet
werden, sollen sie eine erkennbare Bedeutung im Spiel haben.

## Fehlerbehandlung

Das Spiel soll falsche Eingaben freundlich behandeln.

Beispiele:

- leere Eingaben nicht ungeprueft akzeptieren
- unbekannte Befehle mit einem Hinweis beantworten
- bei Auswahlfragen klar sagen, welche Eingaben erlaubt sind

Fehlerbehandlung soll einfach bleiben. Keine komplizierten Validierungs-Systeme.

## Tests und Pruefung

Vor Abschluss einer Aenderung soll geprueft werden:

- Startet das Spiel mit `python main.py`?
- Oeffnet sich das Tkinter-Fenster?
- Kann ein Charakter erstellt werden?
- Fuehrt das Spiel bis zu einem Ende?
- Gibt es keine offensichtlichen Abstuerze bei falschen Eingaben?

Automatisierte Tests sind optional. Wenn Tests geschrieben werden, nur mit
Standardbibliothek, zum Beispiel `unittest`.

## Dokumentation

README.md soll kurz erklaeren:

- was das Projekt ist
- wie man das Spiel startet
- welche Anforderungen umgesetzt wurden

Keine lange Dokumentation schreiben, wenn sie dem Projekt nicht hilft.

## Git-Hinweise

- Keine generierten Dateien committen, wenn sie nicht gebraucht werden.
- Keine `.venv`, IDE-Dateien oder temporaere Render-Dateien committen.
- Aenderungen klein und nachvollziehbar halten.

## Wichtige Einschraenkungen

- Nicht versuchen, ein grosses RPG-System zu bauen.
- Nicht zu viele Features auf einmal einbauen.
- Nicht die Aufgabenstellung ueberkomplizieren.
- Nicht ohne Grund Dependencies hinzufuegen.
- Nicht den Fokus auf Tkinter und lauffaehige Spiellogik verlieren.

Wenn es mehrere moegliche Loesungen gibt, waehle die einfachste Loesung, die die
Anforderung sauber erfuellt.
