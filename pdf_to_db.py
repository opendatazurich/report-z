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


def load_data_in_db(csv_str, c):
    dr = csv.DictReader(StringIO(csv_str), delimiter=',')
    columns = dr.fieldnames
    columns.append('report_text')
    query = insert_db_query(columns)

    for r in dr:
        print(f"Import {r}")
        # download PDF and extract text
        r['report_text'] = rc.download_pdf(r['download_url'])
        db_row = []
        for col in columns:
            db_row.append(r[col])
        # insert into db
        c.execute(query, db_row)


def insert_db_query(columns):
    query = 'INSERT INTO data (\n'
    query += ",\n".join(columns)
    query += ') VALUES ('
    query += ",".join(['?'] * len(columns))
    query += ');'
    return query


conn = None
try:
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

    # load CSV of all annual reports of the City of Zurich
    csv_str = rc.download('https://data.stadt-zuerich.ch/dataset/sar_geschaeftsberichte/download/sar_geschaeftsberichte.csv')
    # load the csv to sqlite db
    load_data_in_db(csv_str, c)

    conn.commit()
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    if conn:
        conn.close()
