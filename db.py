import sqlite3
import os


class DB:
    def __init__(self, db_file: str) -> None:
        self.__db_file = db_file
        if not os.path.isfile(db_file):
            self.__init_db()

    def __init_db(self) -> None:
        # Create tables for the new database.
        try:
            with sqlite3.connect(self.__db_file) as c:
                # Insert table creation queries here.
                pass

        except sqlite3.Error:
            print('DB.__init_db: \
                   An error occurred while initializing a database.')
