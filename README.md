Report-Z
========

Dieses Projekt analysiert die [Geschäftsberichte der Stadt Zürich](https://stadt-zuerich.ch/geschaeftsbericht).

Die Daten stammen vom [Stadtarchiv via Opendata Zürich](https://data.stadt-zuerich.ch/dataset/sar_geschaeftsberichte).

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

Ist im Jupyte Notebook [`WordCloud.ipynb`](https://github.com/metaodi/report-z/blob/master/WordCloud.ipynb) implementiert.

## Suche in den PDFs

# TODO

- [x] WordCloud implementieren
- [ ] Suche über alle PDFs implementieren
