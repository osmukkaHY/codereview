import sqlite3

from config import db_file



def execute(sql: str, *args) -> None:
    with sqlite3.Connection(db_file) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        return conn.execute(sql, args).rowcount


def query(sql: str, *args) -> list[sqlite3.Row]:
    with sqlite3.Connection(db_file) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, args).fetchall()
