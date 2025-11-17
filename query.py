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
    def sql_clause(keyword: str) -> Callable[['Query', str], 'Query']:
        def outer_wrapper (func: Callable[["Query", str], str]) -> Callable[["Query", str], "Query"]:
            def modify_query(query: "Query", argument: str) -> "Query":
                if not isinstance(argument, str):
                    query._error_status = True

                if not query._error_status:
                    query._query_list.append(keyword)
                    query._query_list.append(argument)
                return func(query, argument)
            return modify_query
        return outer_wrapper
        

    @sql_clause('SELECT')
    def select(self, argument: str) -> 'Query':
        return self

    @sql_clause('FROM')
    def from_(self, argument: str) -> 'Query':
        return self

    @sql_clause('WHERE')
    def where(self, argument: str) -> 'Query':
        return self

    @sql_clause('HAVING')
    def having(self, arguent: str) -> 'Query':
        return self

    @sql_clause('ORDER BY')
    def order_by(self, arguent: str) -> 'Query':
        return self

    @sql_clause('LIMIT')
    def limit(self, arguent: str) -> 'Query':
        return self

    @sql_clause('INSERT INTO')
    def insert_into(self, argument: str) -> 'Query':
        return self
    
    @sql_clause('VALUES')
    def values(self, argument: str) -> 'Query':
        return self
    
    @sql_clause('DELETE')
    def delete(self, argument: str) -> 'Query':
        return self

    def execute(self, *args) -> list[tuple] | None:
        if self._error_status:
            return None
        
        result = self._conn.execute(' '.join(self._query_list), args).fetchall()
        return result


def query(conn: sqlite3.Connection) -> Query:
    return Query(conn, [])
