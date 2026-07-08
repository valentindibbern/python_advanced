# Spielkonzept: Das Recht an der Tiefe

## Grundidee

Das Spiel ist ein deutsches, textbasiertes Rollenspiel an einem königlichen
Hof. Im Mittelpunkt steht die Entdeckung einer neuen Höhle, in der wertvolle
Ressourcen vermutet werden. Diese Ressourcen können dem Königreich helfen,
wecken aber auch Gier, politische Interessen und persönliche Pläne.

Der Spieler ist keine der mächtigsten Personen im Reich. Er hat selbst keine
realistische Chance, das Schürfrecht direkt zu erhalten. Trotzdem ist er
wichtig genug, dass andere Figuren seine Unterstützung suchen können. Seine
Beobachtungen, Kontakte und Entscheidungen können später beeinflussen, wer am
Ende profitiert.

Der aktuelle Code setzt den Einstieg in dieses Szenario um:

1. Charakter erstellen
2. Im Ballsaal ankommen
3. Wichtige Personen beobachten
4. Die aktuell implementierte Ballsaal-Szene abschließen

## Setting

Das Spiel spielt in einem mittelalterlich inspirierten Fantasy-Königreich. Der
Königshof ist ein Ort, an dem Macht nicht nur durch Waffen, sondern auch durch
Worte, Titel, Wissen und Beziehungen entsteht.

Die neu entdeckte Höhle liegt in einem bisher wenig beachteten Gebiet des
Reiches. Erste Berichte sprechen von wertvollen Erzen, seltenen Steinen oder
anderen Ressourcen. Noch ist unklar, wie reich die Höhle wirklich ist, wer
Anspruch darauf erheben darf und wie gefährlich eine Ausbeutung wäre.

Um eine offene Auseinandersetzung zu vermeiden, lädt der Hof zu einem Ball
ein. Offiziell ist es ein festlicher Anlass. In Wirklichkeit nutzen die
Teilnehmer den Abend, um Bündnisse zu schließen, Gegner zu schwächen und die
Entscheidung über das Schürfrecht vorzubereiten.

## Aktueller Ablauf

### Szene 1: Charaktererstellung

Die erste Szene liegt in `src/Scenes/scene1/scene.py`.

Der Ablauf ist:

1. Der Spieler gibt einen Namen ein.
2. Der Spieler wählt eine Klasse.
3. Der Spieler wählt eine Spezies.
4. Der Spieler wählt eine Attributverteilung.
5. Der fertige Charakter wird an `Game` zurückgegeben.

Leere Namen werden nicht akzeptiert. Ungültige Choice-IDs führen zu einer
freundlichen Fehlermeldung und die aktuelle Auswahl bleibt bestehen.

### Szene 2: Ankunft im Ballsaal

Die zweite Szene liegt in `src/Scenes/scene2/scene.py`.

Der Spieler betritt den Ballsaal als Baron. Der Herold nennt Titel und Namen
der Figur. Danach kann der Spieler sich im Saal umsehen und fünf wichtige
Personen beobachten:

- Herzogin Alena von Falkenruh
- Graf Bastian von Eisenmark
- Meisterin Runa Steinhand
- Lord Caelion Silberblatt
- Hofsekretär Marik Voss

Jede Person kann einmal beobachtet werden. Beobachtete Personen verschwinden
aus der Auswahl. Nachdem alle fünf Personen beobachtet wurden, kann sich der
Spieler unter die Gäste mischen. Damit endet der aktuell implementierte
Inhalt der Ballsaal-Szene.

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

Das Ziel-Feld existiert bereits in den Charakterdaten, wird im aktuellen Code
aber noch nicht automatisch durch die Klasse gesetzt.

## Klassen

Die Klasse bestimmt aktuell vor allem die Identität der Figur. Ein eigener
Attributbonus oder ein eigenes Klassenziel wird im Code noch nicht vergeben.

### Aufsteiger

Der Aufsteiger sieht die Höhle als Chance, seine Stellung zu verbessern und
wirtschaftlich oder politisch aufzusteigen.

### Intrigant

Der Intrigant interessiert sich weniger für die Höhle selbst. Er sieht sie als
Werkzeug, um Konkurrenten zu schwächen oder geheime Interessen aufzudecken.

### Netzwerker

Der Netzwerker will Kontakte knüpfen, Vertrauen aufbauen und seine Stellung am
Hof langfristig verbessern.

## Spezies

Die Spezies beeinflusst aktuell die Startattribute.

### Mensch

Menschen erhalten einen Bonus auf Schlagfertigkeit.

### Elf

Elfen erhalten einen Bonus auf Verständnis.

### Zwerg

Zwerge erhalten einen Bonus auf Wissen.

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

### Graf Bastian von Eisenmark

Bastian steht für schnellen Gewinn und sichtbaren Ehrgeiz. Er verspricht
Reichtum und Arbeit, wirkt aber riskant und rücksichtslos.

### Meisterin Runa Steinhand

Runa steht für Fachwissen, Bergbau und Gildeninteressen. Sie will, dass
Bergleute und Handwerker beim Schürfrecht mitentscheiden.

### Lord Caelion Silberblatt

Caelion beobachtet alte Abmachungen, verborgene Ängste und mögliche
diplomatische Gefahren.

### Hofsekretär Marik Voss

Marik ist offiziell neutral, weiß aber vermutlich mehr über Ansprüche,
Einladungen und alte Schriftstücke, als er offen sagt.

## Technische Umsetzung

`Game` lädt Szenen über eine einfache `_load_scene`-Methode. Die aktuelle Szene
verarbeitet Texteingaben und Auswahlentscheidungen. Wenn eine Szene fertig ist,
holt `Game` den aktuellen `Player` aus der Szene und startet die nächste Szene.

Die Tkinter-Oberfläche kennt keine Details der Spiellogik. Sie zeigt nur die
`GameResponse` an und sendet Texteingaben oder Choice-IDs als `UiResponse`
zurück.

## Aktuelle Grenze

Nach der Ballsaal-Szene ist im Code noch keine dritte Szene vorhanden. Der
Code versucht nach dem Abschluss der Ballsaal-Szene aktuell trotzdem, die
nächste Szene mit ID `2` zu laden. Solange diese Szene oder eine saubere
Ende-Behandlung fehlt, ist das die technische Grenze des Spielverlaufs.
