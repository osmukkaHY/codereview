import sqlite3
import os

from config import  db_file, db_schema_file


class DB:
    def __init__(self) -> None:
        self.__db_file = db_file
        if not os.path.isfile(db_file):
            self.__init_db()


    def __init_db(self) -> None:
        # Create tables for the new database.
        with open(db_schema_file, 'r') as file:
            script = file.read()
        try:
            with sqlite3.connect(self.__db_file) as conn:
                conn.executescript(script)

        except sqlite3.Error:
            print('DB.__init_db: '
                  'An error occurred while initializing a database.')


    def execute(self, query: str, args: list[str]=[]) -> list[tuple] | None:
        try:
            with sqlite3.connect(self.__db_file) as conn:
                result = conn.execute(query, args).fetchall()
        except sqlite3.OperationalError:
            print('DB.execute: '
                 f'Couldn\'t execute query "{query}" with arguments {args}')
            result = None
            
        return result

