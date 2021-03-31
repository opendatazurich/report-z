#!/usr/bin/env python3

# This script creates a new sqlite database based on the downloaded CSV

import sqlite3
import traceback
import os
import sys
import csv
from io import StringIO
import report_common as rc

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


def load_csv(csv_str):
    dr = csv.DictReader(StringIO(csv_str), delimiter=',')
    columns = dr.fieldnames
    columns.append('report_text')
    to_db = []
    for r in dr:
        print(r)
        # download PDF and extract text
        r['report_text'] = rc.download_pdf(r['download_url'])
        print(r['report_text'])
        db_row = []
        for col in columns:
            db_row.append(r[col])
        to_db.append(db_row)
    return columns, to_db


def insert_db_query(columns):
    query = 'INSERT INTO data (\n'
    query += ",\n".join(columns)
    query += ') VALUES ('
    query += ",".join(['?'] * len(columns))
    query += ');'
    return query

# load CSV of all annual reports of the City of Zurich
csv_str = rc.download('https://data.stadt-zuerich.ch/dataset/sar_geschaeftsberichte/download/sar_geschaeftsberichte.csv')

conn = None
try:
    # load the csv to sqlite db
    columns, to_db = load_csv(csv_str)
    
    sys.exit(1)

    # create db
    DATABASE_NAME = os.path.join(__location__, 'data.sqlite')
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS data')
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS data (
            signatur text NOT NULL PRIMARY KEY,
            titel text,
            jahr integer,
            link_query  text,
            dateiname text,
            download_url text,
            report_text text
        )
        '''
    )
    
    # insert into db
    query = insert_db_query(columns)
    c.executemany(query, to_db)
    conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    if conn:
        conn.close()
