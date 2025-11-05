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
        if result == None:
            return None
        return bool(result[0][0])
