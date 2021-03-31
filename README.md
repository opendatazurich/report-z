Report-Z
========

Dieses Projekt analysiert die Geschäftsberichte der Stadt Zürich.

Die Daten stammen vom Stadtarchiv via Opendata Zürich.

# Installation

```
./setup.sh
```

Das Projekt setzt voraus, dass `pdftotext` installiert ist, am einfachsten lässt sich dies via poppler-utils installieren:


```
sudo apt-get install poppler-utils
```


# Anwendung

Virtualenv laden:

```
source ./pyenv/bin/activate
```


## Daten laden

```
python pdf_to_db.py
```

## WordCloud erstellen

## Suche in den PDFs

# TODO

- [] WordCloud implementieren
- [] Suche über alle PDFs implementieren
