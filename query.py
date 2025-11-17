from dataclasses import dataclass
from enum import Enum
import sqlite3


class QueryType(Enum):
    SELECT = 0
    INSERT = 1
    UPDATE = 2
    DELETE = 3


@dataclass
class Query:
    _conn:         sqlite3.Connection
    _query_list:   list[str]
    _query_type:   QueryType   = None
    _error_status: bool        = False

    def select(self, argument: str):
        if not isinstance(argument, str):
            self._error_status = True
        if self._error_status:
            return self
        
        self._query_list.append('SELECT')
        self._query_list.append(argument)
        return self

    def from_(self, argument: str):
        if not isinstance(argument, str):
            self._error_status = True
        if self._error_status:
            return self
        
        self._query_list.append('FROM')
        self._query_list.append(argument)
        return self

    def where(self, argument: str):
        if not isinstance(argument, str):
            self._error_status = True
        if self._error_status:
            return self
        
        self._query_list.append('WHERE')
        self._query_list.append(argument)
        return self
    
    def execute(self, *args) -> list[tuple] | None:
        if self._error_status:
            return None
        
        result = self._conn.execute(' '.join(self._query_list), args).fetchall()
        return result


def query(conn: sqlite3.Connection) -> Query:
    return Query(conn, [])
