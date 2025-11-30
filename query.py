from dataclasses import dataclass
import sqlite3
from typing import Callable

from config import db_file


@dataclass
class Query:
    _query_list: list[str]
 
    """Appends a keyword and its arguments to the query.
    """
    @staticmethod
    def sql_clause(keyword: str) -> Callable[['Query', str], 'Query']:
        def outer_wrapper (func: Callable[["Query", str], str]) -> Callable[["Query", str], "Query"]:
            def append_query(query: "Query", argument: str) -> "Query":
                
                query._query_list.append(keyword)
                query._query_list.append(argument)
                
                return func(query, argument)
            return append_query
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
    def having(self, argument: str) -> 'Query':
        return self


    @sql_clause('ORDER BY')
    def order_by(self, argument: str) -> 'Query':
        return self


    @sql_clause('LIMIT')
    def limit(self, argument: str) -> 'Query':
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


    @sql_clause('UPDATE')
    def update(self, argument: str) -> 'Query':
        return self


    @sql_clause('SET')
    def set(self, argument: str) -> 'Query':
        return self
        

    def execute(self, *args) -> sqlite3.Cursor:
        with sqlite3.Connection(db_file) as conn:
            result = conn.execute(' '.join(self._query_list), args)
        return result

def query() -> Query:
    return Query([])
