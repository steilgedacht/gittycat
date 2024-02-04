# Gittycat
```
<ASCII art goes here>
```

Gittycat ist dein Tamagothi für Git. Eine liebenswerte Katze die in deinem Repository lebt, 
versorgt werden muss und dich idealerweise eine emotionale Bindung zu deinem Code aufbauen lässt.

## Funktionsweise - Gameplay
Deine Katze braucht Pflege. Sie wird älter und älter und du musst dich um sie kümmern.
Die Bedürfnisse/Eigenschaften der Katze sind:
- Food: Die Katze wird über die Zeit hungrig. Jedes mal wenn du einen Commit machst, wird deine Katze gefüttert.
- Excitement: Katzen müssen unterhalten werden und langweilen sich mit der Zeit. Jede neue Zeile Code die du schreibst, ist spannend und erhöht das Interesse deiner Katze.
- Energy: Anstrengung macht müde. Und wie wir in Missing Semester gelernt haben ist jedes Öffnen einer Datei aufwändig und anstrengend. Jede geänderte Datei kostet die Katze Energie. Zum Glück schläft sie den meisten Tag und erholt sich.
- Evolution: Mit der Zeit entwickelt sich deine Katze weiter. Du adoptierst ein Kätzchen. Nach einer gewissen Anzahl an Tagen wird sie erwachsen.
    - keie Auswirkung auf das Gameplay, aber neues cooles Ascii-Art

## Funktionsweise - Technisch
Durch die Installation von Gittycat in ein Repository wird ein neuer Unterordner `.gittycat` erstellt, in dem die Katze lebt.
Dort ist sie als JSON-Datei abgespeichert und alle Parameter sind auch manuell editierbar.

## Installation
```bash
# make sure git is installed
sudo apt install git
# Install necessary python dependencies
pip install -r requirements.txt
```

## Nutzung

### Allgemein
```bash
# Inside main directory of your git repository
python3 <path to gittycat>/gittycat.py <command>
# Get a list of commands
python3 <path to gittycat>/gittycat.py --help
```

### Adoptieren
Beim Adoptieren deiner Katze kannst du ihr einen Namen geben (den du dir merken musst, aber wer vergisst schon den Namen seiner Katze?).
Die Katze commitet sich dann selbstständig in dein Repository.

Zusätzlich kannst du ihre Persönlichkeit auswählen. Die Persönlichkeit bestimmt, wie schnell/stark die Bedürfnisse der Katze geändert werden.
(zumindest könntest du das theoretisch, aktuell gibt es nur das Default-Profil. Erstell doch deine eigenen unter `gittycat/personalities`).
Die Persönlichkeit kannst du später auch manuell in der JSON-Datei unter `.gittycat/cats` ändern.

```bash
# Adopt a new cat

# Inside main directory of your git repository
python3 <path to gittycat>/gittycat.py adopt Garfield -p default
```

### Check-In
Zur Überprüfung, wie es deiner Katze geht, benutze den `gittycat status` Command.
```bash
# Check the status of your cat

# Inside main directory of your git repository
python3 <path to gittycat>/gittycat.py status Garfield
```

### Aktualisierung
Um die Bedürfnisse deiner Katze anzupassen und alle Commits seit dem letzten Mal zu verarbeiten, benutze den
`gittycat update` Command. Nach dem Update kriegst du auch gleich die Statusmeldung über den neuen Zustand
deiner Katze.

```bash
# Update the status of your cat
python3 <path to gittycat>/gittycat.py update Garfield
```

### Streicheln
Katzen streichen ist schön. Katzen streicheln ist wichtig. Katzen streicheln ist notwendig.

Erhöht das Excitement-Level deiner Katze und macht sie bestimmt sehr glücklich.

```bash
# Pet your cat
python3 <path to gittycat>/gittycat.py pet Garfield
```

### Nickerchen
Katzen schlafen viel. Du als Programmierer eher weniger.
Wenns wieder eine long Coding Night wird, geht deiner Katze vielleicht unterwegs die Energie aus.
Dann kannst du ihr Energy-Level mit dem `gittycat nap` manuell erhöhen.

```bash
# Let your cat take a nap
python3 <path to gittycat>/gittycat.py nap Garfield
```

### Freilassen
Katzen sind freiheitsliebende Tiere. Wenn das Ende eurer gemeinsamen Reise gekommen ist, kannst du sie mit dem `gittycat release` Command freilassen.

Dadurch wird Gittycat aus deinem Repository entfernt. Lediglich die Erinnerung an eine gute Zeit
(*und viele, viele "Gittycat | updated my needs" commits*) bleiben zurück.

```bash
# Release your cat
python3 <path to gittycat>/gittycat.py release Garfield
```