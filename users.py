from werkzeug.security import check_password_hash

from db import DB


class Users:
    def __init__(self) -> None:
        self.__db = DB()

    
    def exists(self, username: str) -> bool | None:
        result = self.__db.fetch("""SELECT EXISTS(
                                        SELECT 1
                                        FROM Users
                                        WHERE username = ?
                                    );""", username)
        return None if result == None else bool(result[0][0])
    

    def validate(self, username: str, password: str) -> bool | None:
        if not self.exists(username): return False
        
        result = self.__db.fetch("""SELECT username, password_hash
                                    FROM Users
                                    WHERE username = ?
                                    ;""", username)
        if result == None: return False
        password_hash = result[0][1]

        return True if check_password_hash(password_hash, password) else False

    

    def add(self, username: str, password_hash: str) -> bool | None:
        if self.exists(username):
            return False
        return self.__db.insert("""INSERT INTO
                                      Users (username, password_hash)
                                      VALUES (?, ?)""", username,
                                                        password_hash)
