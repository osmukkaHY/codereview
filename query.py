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
    _conn:             sqlite3.Connection
    _query_list:       list[str]
    _query_type:       QueryType   = None
    _last_keyword:     str         = None
    _error_message:    str         = None
 
    """Tells that the clause cant be the root of a SQL query.
    """
    @staticmethod
    def purely_descriptive(func: Callable[["Query", str], str]) -> Callable[["Query", str], str]:
        def wrapper(query: 'Query', argument: str) -> "Query":
            if not query._query_type:
                query._error_message = True
            else:
                func(query, argument)
            return query
        return wrapper
                

    @staticmethod
    def sql_clause(keyword: str, binds_to: list[str]=None) -> Callable[['Query', str], 'Query']:
        binds_to = [None] if not binds_to else binds_to
        def outer_wrapper (func: Callable[["Query", str], str]) -> Callable[["Query", str], "Query"]:
            def append_query(query: "Query", argument: str) -> "Query":
                
                # If keyword has to be first but isn't.
                if query._query_type and binds_to == [None]:
                    query._error_message = True

                # If the given argument is not a string.
                if not isinstance(argument, str):
                    query._error_message = True
                if not query._error_message:
                    if not query._query_type:
                        query._query_type = {
                            'SELECT': QueryType.SELECT,
                            'INSERT': QueryType.INSERT,
                            'UPDATE': QueryType.UPDATE,
                            'DELETE': QueryType.DELETE
                        }[keyword]
                    query._query_list.append(keyword)
                    query._query_list.append(argument)
                query._last_keyword = keyword
                print(query)
                return func(query, argument)
            return append_query
        return outer_wrapper
    
    
    @sql_clause('SELECT', binds_to=['DELETE'])
    def select(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('FROM', binds_to=['SELECT'])
    def from_(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('WHERE', binds_to=['FROM'])
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

    def execute(self, *args) -> list[tuple] | str:
        if self._error_message:
            return self._error_message
        
        result = self._conn.execute(' '.join(self._query_list), args).fetchall()
        return result


def query(conn: sqlite3.Connection) -> Query:
    return Query(conn, [])
