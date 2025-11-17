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


    def add(self, username: str, password_hash: str) -> bool:
        if self.exists(username):
            return False
        return True if query().insert_into('Users (username, password_hash)')  \
                              .values('(?, ?)')                                \
                              .execute(username, password_hash)                \
                              .lastrowid                                       \
        else False


    def delete(self, username: str) -> bool:
        if not self.exists(username):
            return False
        
        return True if query().delete('')              \
                              .from_('Users')          \
                              .where('username = ?')   \
                              .execute(username)       \
                              .rowcount                \
        else False
