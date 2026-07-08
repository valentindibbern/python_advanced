# Spielkonzept: Das Recht an der Tiefe

## Grundidee

Das Spiel ist ein deutsches, textbasiertes Rollenspiel an einem königlichen
Hof. Im Mittelpunkt steht die Entdeckung einer neuen Höhle, in der wertvolle
Ressourcen vermutet werden. Diese Ressourcen können dem Königreich helfen,
wecken aber auch Gier, politische Interessen und persönliche Pläne. Die Höhle
ist außerdem gefährlich: Wer sie kontrolliert, erhält nicht nur Reichtum,
sondern auch Verantwortung für Arbeiter, alte Rechte und mögliche Schäden.

Der Spieler ist keine der mächtigsten Personen im Reich. Er hat selbst keine
realistische Chance, das Schürfrecht direkt zu erhalten. Trotzdem ist er
wichtig genug, dass andere Figuren seine Unterstützung suchen können. Seine
Beobachtungen, Kontakte und Entscheidungen können später beeinflussen, wer am
Ende profitiert.

Der aktuelle Code setzt dieses Szenario als vollständigen kurzen Ballabend um:

1. Startbildschirm anzeigen
2. Charakter erstellen
3. Im Ballsaal ankommen
4. Wichtige Personen beobachten
5. Ein politisches Gespräch führen
6. Vor dem Königspaar reagieren
7. Im Rat eine Allianz unterstützen
8. Am Ende erfahren, ob das persönliche Ziel erreicht wurde

## Setting

Das Spiel spielt in einem mittelalterlich inspirierten Fantasy-Königreich. Der
Königshof ist ein Ort, an dem Macht nicht nur durch Waffen, sondern auch durch
Worte, Titel, Wissen und Beziehungen entsteht.

Die neu entdeckte Höhle liegt in einem bisher wenig beachteten Gebiet des
Reiches. Erste Berichte sprechen von wertvollen Erzen, seltenen Steinen oder
anderen Ressourcen. Noch ist unklar, wie reich die Höhle wirklich ist, wer
Anspruch darauf erheben darf und wie gefährlich eine Ausbeutung wäre.
Gerade diese Unsicherheit macht den Ballabend angespannt. Manche Figuren reden
von Gewinn, andere von Schuld, Einsturzgefahr oder vergessenen Verträgen.

Um eine offene Auseinandersetzung zu vermeiden, lädt der Hof zu einem Ball
ein. Offiziell ist es ein festlicher Anlass. In Wirklichkeit nutzen die
Teilnehmer den Abend, um Bündnisse zu schließen, Gegner zu schwächen und die
Entscheidung über das Schürfrecht vorzubereiten.

## Aktueller Ablauf

### Szene 0: Startbildschirm

Die Startszene liegt in `src/Scenes/scene0/scene.py`.

Sie wird direkt beim Laden des Fensters angezeigt. Der Spieler startet die
Charaktererstellung über den Button `Start` im Bereich `Spiel` unten rechts.
Der Button `Stop` schließt das Fenster.

### Szene 1: Charaktererstellung

Die Charaktererstellung liegt in `src/Scenes/scene1/scene.py`.

Der Ablauf ist:

1. Der Spieler gibt einen Namen ein.
2. Der Spieler wählt eine Klasse.
3. Der Spieler wählt eine Spezies.
4. Der Spieler wählt eine Attributverteilung.
5. Der fertige Charakter wird an `Game` zurückgegeben.

Die Szene ist erzählerisch in die Welt eingebunden. Der Spieler wählt nicht
nur Werte, sondern auch eine Motivation für den Ballabend. Klasse, Spezies und
Attribute werden mit kurzen Texten erklärt, damit der Konflikt vor dem
Ballsaal verständlich wird.

Leere Namen werden nicht akzeptiert. Ungültige Choice-IDs führen zu einer
freundlichen Fehlermeldung und die aktuelle Auswahl bleibt bestehen.

### Szene 2: Ballabend und Schürfrecht

Die zweite Szene liegt in `src/Scenes/scene2/scene.py`.

Der Spieler betritt den Ballsaal als Baron. Der Herold nennt Titel und Namen
der Figur. Danach kann der Spieler sich im Saal umsehen und wichtige Personen
beobachten:

- Herzogin Alena von Falkenruh
- Graf Bastian von Eisenmark
- Meisterin Runa Steinhand
- Lord Caelion Silberblatt
- Hofsekretär Marik Voss

Jede Person kann einmal beobachtet werden. Beobachtete Personen verschwinden
aus der Auswahl. Nachdem mindestens drei Personen beobachtet wurden, kann der
Spieler ein erstes Gespräch beginnen. Danach folgt ein kurzer Auftritt des
Königspaars, eine Entscheidung im Rat und am Ende die Verkündung der
Schürfrechte.

Die zuerst beobachtete Person wird in `story_flags["first_observed_npc"]`
gespeichert. Später erinnert sich der Spieler an diese erste Beobachtung.
Dadurch wirken frühe Hinweise stärker und die Geschichte reagiert sichtbarer
auf die Entscheidung des Spielers.

## Spielerfigur

Die Spielerfigur hat aktuell immer den Titel `Baron`.

Gespeicherte Daten:

- Name
- Titel
- Spezies
- Klasse
- Wissen
- Schlagfertigkeit
- Verständnis
- Ziel
- Zielstatus

Das Ziel wird nach Klasse und Spezies automatisch gesetzt. Der Zielstatus wird
im Ballabend aktualisiert, aber erst am Ende endgültig bewertet.

## Klassen

Die Klasse bestimmt das persönliche Ziel der Figur.

### Aufsteiger

Der Aufsteiger sieht die Höhle als Chance, seine Stellung zu verbessern und
wirtschaftlich oder politisch aufzusteigen.
Er will, dass der eigene Name am Hof mehr Gewicht bekommt.

Ziel: Die eigene Spezies soll Teil der Allianz sein, die am Ende die
Schürfrechte erhält. Menschen gehören zur Hofallianz, Zwerge zum Gildenpakt
und Elfen zur Gesandtschaft. Der gemeinsame Kronenpakt zählt für dieses Ziel
ebenfalls als Erfolg.

### Intrigant

Der Intrigant interessiert sich weniger für die Höhle selbst. Er sieht sie als
Werkzeug, um Konkurrenten zu schwächen oder geheime Interessen aufzudecken.
Sein Ziel ist ein Erfolg, den möglichst niemand direkt auf ihn zurückführen
kann.

Ziel: Der Rivale darf am Ende nicht Teil der entscheidenden Allianz sein. Bei
einem menschlichen Spieler ist der Rivale ein Mensch, bei einem Zwerg ein Elf
und bei einem Elf ein Zwerg.

### Netzwerker

Der Netzwerker will Kontakte knüpfen, Vertrauen aufbauen und seine Stellung am
Hof langfristig verbessern.
Für ihn ist ein richtiger Kontakt wertvoller als eine laute Rede.

Ziel: Der Netzwerker will neue Freundschaften schließen und dadurch eine
Person des Königspaars erreichen. Menschen suchen dafür Kontakt zu einem Zwerg
oder Elf. Zwerge und Elfen suchen dafür Kontakt zu einem Menschen.

## Spezies

Die Spezies beeinflusst aktuell die Startattribute.

### Mensch

Menschen erhalten einen Bonus auf Schlagfertigkeit.
Sie sind nahe am Hof, aber dadurch auch stärker in Gefallen, Gerüchte und
Absprachen verwickelt.

### Elf

Elfen erhalten einen Bonus auf Verständnis.
Sie bringen alte Rechte und Erinnerungen mit, denen der Hof höflich zuhört,
aber nicht immer vertraut.

### Zwerg

Zwerge erhalten einen Bonus auf Wissen.
Sie kennen Stein, Stollen und Gefahr besser als der Adel, müssen aber darum
kämpfen, nicht nur als Werkzeug des Hofes behandelt zu werden.

## Attribute

Die Attribute beschreiben, wie der Spieler mit sozialen und politischen
Situationen umgehen kann.

### Wissen

Wissen steht für Kenntnisse über Personen, Titel, politische Zusammenhänge,
alte Rechte und den möglichen Wert der Höhle.

### Schlagfertigkeit

Schlagfertigkeit steht für schnelle Antworten, überzeugendes Auftreten und
Reaktionen in Gesprächen unter Druck.

### Verständnis

Verständnis steht für Einfühlungsvermögen, das Erkennen von Motiven und das
Lesen unausgesprochener Absichten.

## Attributverteilung

Die Attributverteilung wird in der Charaktererstellung gewählt.

Der Spieler wählt ein Hauptattribut. Dieses Hauptattribut erhält 2 Punkte. Die
beiden anderen Attribute erhalten je 1 Punkt. Danach wird der Speziesbonus
addiert:

- Mensch: +1 Schlagfertigkeit
- Elf: +1 Verständnis
- Zwerg: +1 Wissen

Beispiel:

Ein Elf mit Hauptattribut Wissen erhält:

- Wissen: 2
- Schlagfertigkeit: 1
- Verständnis: 2

## NPCs im aktuellen Code

### Herzogin Alena von Falkenruh

Alena steht für Kontrolle und Vorsicht. Sie möchte verhindern, dass ein
einzelnes Adelshaus durch das Schürfrecht zu mächtig wird.
Sie fürchtet besonders Verträge, die der Hof später nicht mehr brechen kann.

### Graf Bastian von Eisenmark

Bastian steht für schnellen Gewinn und sichtbaren Ehrgeiz. Er verspricht
Reichtum und Arbeit, wirkt aber riskant und rücksichtslos.
Er merkt sich, wer nicht über seine Witze lacht oder seinen Mut bewundert.

### Meisterin Runa Steinhand

Runa steht für Fachwissen, Bergbau und Gildeninteressen. Sie will, dass
Bergleute und Handwerker beim Schürfrecht mitentscheiden.
Ihre Warnungen machen klar, dass die Höhle auch körperlich gefährlich ist.

### Lord Caelion Silberblatt

Caelion beobachtet alte Abmachungen, verborgene Ängste und mögliche
diplomatische Gefahren.
Für ihn können alte Verträge zu Waffen werden.

### Hofsekretär Marik Voss

Marik ist offiziell neutral, weiß aber vermutlich mehr über Ansprüche,
Einladungen und alte Schriftstücke, als er offen sagt.
Seine Mappe enthält Hinweise, die für mehrere Seiten gefährlich werden können.

### Königin Meridia

Meridia leitet den Abend politisch. Sie hört kurz eine Stimme aus dem Saal an
und bewertet, wer Verantwortung statt nur Gewinn verspricht.
Ihre Frage wirkt wie eine Prüfung des ganzen Saals.

### König Arwed

Arwed verkündet am Ende die Entscheidung über die Schürfrechte. Er spricht
weniger als Meridia, steht aber für die rechtliche Autorität der Krone.

## Technische Umsetzung

`Game` lädt Szenen über eine einfache `_load_scene`-Methode. Die aktuelle Szene
verarbeitet Texteingaben und Auswahlentscheidungen. Wenn eine Szene fertig ist,
holt `Game` den aktuellen `Player` aus der Szene und startet die nächste Szene.
Wenn keine weitere Szene vorhanden ist, gibt `Game` die vorhandene Endantwort
der Szene zurück und setzt den Zustand auf `FINISHED`.

Die Tkinter-Oberfläche kennt keine Details der Spiellogik. Sie zeigt nur die
`GameResponse` an und sendet Texteingaben oder Choice-IDs als `UiResponse`
zurück. Die Buttons `Start` und `Stop` sind Steuerknöpfe der Oberfläche und
keine normalen Spiel-Choices.

## Ende

Das Spiel endet nach der Verkündung im Ballsaal. Es gibt danach keine weitere
Handlungsszene. Die Endmeldung enthält die siegreiche Allianz und den
Zielstatus des Spielers. Zusätzlich erhält der Spieler eine kurze persönliche
Auswertung, die zur gewählten Klasse passt.
