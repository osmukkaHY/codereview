from werkzeug.security import check_password_hash

from db import DB
from query import query


class Users:
    def __init__(self) -> None:
        self.__db = DB()

    
    def exists(self, username: str) -> bool:
        return True if query().select('1')             \
                              .from_('Users')          \
                              .where('username = ?')   \
                              .execute(username)       \
                              .fetchone()              \
        else False
    

    def validate(self, username: str, password: str) -> bool:
        if not self.exists(username):
            return False
        password_hash = query().select('username, password_hash')  \
                               .from_('Users')                     \
                               .where('username = ?')              \
                               .execute(username)                  \
                               .fetchone()[1]

        return check_password_hash(password_hash, password)

    

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
