from werkzeug.security import check_password_hash

from db import DB
from query import query


class Users:
    def __init__(self) -> None:
        self.__db = DB()

    
    def exists(self, username: str) -> bool:
        result = query().select('1') \
                        .from_('Users') \
                        .where('username = ?') \
                        .execute(username) \
                        .fetchall()
        return True if len(result) else False
    

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
    

    def delete(self, username: str, password: str) -> bool | None:
        if not self.exists(username):
            return False
        
        return self.__db.insert("""DELETE FROM Users
                                   WHERE username = ?
                                   ;""", username)
