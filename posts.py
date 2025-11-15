from dataclasses import dataclass

from db import DB

@dataclass
class Post:
    timestamp:  str
    username:   str
    title:      str
    context:    str
    content:    str


class Posts:
    def __init__(self):
        self._db = DB()

    def new(self,
            username:   str,
            title:      str,
            context:    str,
            content:    str) -> bool | None:
        user_id = self._db.fetch('SELECT id FROM Users WHERE username = ?;',
                                 username)[0][0]
        self._db.insert("""INSERT INTO Posts (poster_id, title, context, content)
                           VALUES (?, ?, ?, ?);""", user_id,
                                                    title,
                                                    context,
                                                    content)
