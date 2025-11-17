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
                query._error_message = 'Cannot start a query with a purely descriptive keyword.'
            else:
                func(query, argument)
            return query
        return wrapper

    """Appends a keyword and its arguments to the query and returns an error if needed.
    """
    @staticmethod
    def sql_clause(keyword: str, binds_to: list[str]=None) -> Callable[['Query', str], 'Query']:
        binds_to = [None] if not binds_to else binds_to
        def outer_wrapper (func: Callable[["Query", str], str]) -> Callable[["Query", str], "Query"]:
            def append_query(query: "Query", argument: str) -> "Query":
                
                # If keyword has to be first but isn't.
                if query._query_type and binds_to == [None]:
                    query._error_message = f'Keyword {keyword} must be first in a query'

                # If the given argument is not a string.
                if not isinstance(argument, str):
                    query._error_message = f'Clause argument cannot be of type {type(argument)}'

                # append the clause if no errors were found.
                if not query._error_message:
                    # @purely_descriptive makes sure this triggers only on correct keywords.
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
                return func(query, argument)
            return append_query
        return outer_wrapper
    
    
    @sql_clause('SELECT', binds_to=['INSERT INTO'])
    def select(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('FROM', binds_to=['SELECT', 'DELETE'])
    def from_(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('WHERE', binds_to=['FROM'])
    def where(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('HAVING', binds_to=['FROM', 'WHERE'])
    def having(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('ORDER BY', binds_to=['FROM', 'WHERE', 'HAVING'])
    def order_by(self, argument: str) -> 'Query':
        return self

    @purely_descriptive
    @sql_clause('LIMIT', binds_to=['FROM', 'WHERE', 'HAVING'])
    def limit(self, argument: str) -> 'Query':
        return self

    @sql_clause('INSERT INTO')
    def insert_into(self, argument: str) -> 'Query':
        return self
    
    @purely_descriptive
    @sql_clause('VALUES', binds_to=['INSERT INTO'])
    def values(self, argument: str) -> 'Query':
        return self
    
    @sql_clause('DELETE')
    def delete(self, argument: str) -> 'Query':
        return self

    def execute(self, *args) -> list[tuple] | int | str:
        if self._error_message:
            return self._error_message
        
        result = self._conn.execute(' '.join(self._query_list), args)

        match self._query_type:
            case QueryType.SELECT:
                return result.fetchall()
            case QueryType.INSERT:
                return result.lastrowid
            case QueryType.UPDATE | QueryType.DELETE:
                return result.rowcount



def query(conn: sqlite3.Connection) -> Query:
    return Query(conn, [])
