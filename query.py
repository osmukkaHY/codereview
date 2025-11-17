from dataclasses import dataclass
from enum import Enum
import sqlite3
from typing import Callable


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

    @staticmethod
    def sql_clause(func: Callable[["Query", str], str]) -> Callable[["Query", str], "Query"]:
        def wrapper(self: "Query", argument: str) -> "Query":
            if not isinstance(argument, str):
                self._error_status = True

            if not self._error_status:
                keyword = func(self, argument)
                self._query_list.append(keyword)
                self._query_list.append(argument)
            return self
        return wrapper

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
