# Szene 0: Startbildschirm

Diese Datei beschreibt den Startbildschirm des Spiels.
Die konkrete Szene liegt in `src/Scenes/scene0/scene.py`.

## Zweck

Szene 0 wird direkt angezeigt, wenn das Tkinter-Fenster geladen ist.
Sie ist noch keine eigentliche Spielhandlung, sondern erklärt kurz den Start.

Der Spieler beginnt das Spiel nicht durch Texteingabe oder eine normale
Choice, sondern über den Button `Start` im Bereich `Spiel` unten rechts.

## Ablauf

1. `Ui` erstellt das Fenster.
2. `Game.start()` gibt die Startszene zurück.
3. Die UI zeigt den Starttext im History-Bereich an.
4. Die Texteingabe bleibt deaktiviert.
5. Im rechten unteren Grid-Bereich stehen die Buttons `Start` und `Stop`.
6. `Start` ruft `Game.start_game()` auf.
7. `Game.start_game()` lädt Szene 1 und startet die Charaktererstellung.
8. `Stop` schließt das Tkinter-Fenster.

## Schnittstelle zu Game

Die Startszene gibt eine normale `GameResponse` zurück.

Wichtige Werte:

- Titel: `Start`
- Message-ID: `game-start-screen`
- Eingabemodus: `InputMode.NONE`
- Keine Choice-IDs

## Schnittstelle zur UI

Die UI behandelt `Start` und `Stop` als Steuerknöpfe, nicht als Spiel-Choices.

- `Start` startet die Charaktererstellung und wird danach deaktiviert.
- `Stop` ruft `root.destroy()` auf und beendet das Fenster.

## Abgrenzung

Szene 0 verändert keine Charakterdaten und setzt keine Story-Flags.
Die eigentliche Spielerstellung beginnt erst in Szene 1.
