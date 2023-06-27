import sqlite3
import pandas as pd
from sqlite3 import Error
import os



def connect_db():
    connection = None
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "db.db"
    abs_file_path = os.path.join(script_dir, rel_path)
    try:
        connection = sqlite3.connect(abs_file_path, check_same_thread=False)
    except sqlite3.Error as err:
        print(f"The error '{err}' occurred during 'connection to database' in connect_sqlite3")
    return connection


def get_apple(id):
    conn = connect_db()
    sql = f"SELECT * FROM apples WHERE id = {id}"
    result = pd.read_sql_query(sql, conn)
    conn.close()
    return result

def get_apples(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT pollination FROM apples WHERE id = {id}")
    row = cur.fetchall()
    id_list = ",".join(row[0])
    sql = f"SELECT * FROM apples WHERE id IN (" + id_list + ")"
    result = pd.read_sql_query(sql, conn)
    conn.close()
    return result

"""
Populate Dropdown Menu (Species)
"""


def build_search():
    try:
        conn = connect_db()
        sql = f"SELECT id, name, latin_name FROM apples"
        df = pd.read_sql_query(sql, conn)
        conn.close()
        df = df.rename(columns={"id": "value", "name": "label"})
        df["label"] = df['label'].astype(str) + " (Latin: " + df["latin_name"].astype(str) + ")"
        df.drop(labels="latin_name", axis="columns", inplace=True)
        df.set_index("value")
        search_dict = df.to_dict("records")
        return search_dict
    except sqlite3.Error as err:
        print(f"The error '{err}' occurred during build_search")