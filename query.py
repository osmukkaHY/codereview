from dataclasses import dataclass
import sqlite3


@dataclass
class Query:
    _conn:         sqlite3.Connection
    _query_list:   list[str]
    _error_status: bool = False

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


def query(conn: sqlite3.Connection) -> Query:
    return Query(conn, [])
