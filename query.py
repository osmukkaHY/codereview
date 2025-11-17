from dataclasses import dataclass
import sqlite3


@dataclass
class Query:
    _conn:         sqlite3.Connection
    _query_list:   list[str]
    _error_status: bool = False



def query(conn: sqlite3.Connection) -> Query:
    return Query(conn, [])
