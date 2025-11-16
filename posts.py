from dataclasses import dataclass

from db import DB

@dataclass
class Post:
    id:         str
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

    def n_recent(self, n: int):
        post_tuples = self._db.fetch("""SELECT *
                                        FROM Posts
                                        ORDER BY ts
                                        LIMIT ?;""", n)
        posts = []
        for post in post_tuples:
            username = self._db.fetch("""SELECT username
                                         FROM Users
                                         WHERE id = ?;""", post[2])[0][0]
            posts.append(Post(post[0], post[1], username, post[3], post[4], post[5]))
        return posts

    def by_user(self, username: str) -> list[Post]:
        post_tuples = self._db.fetch("""SELECT *
                                        FROM Posts
                                        WHERE username = ?;""", username)
        posts = []
        for post in post_tuples:
            posts.append(Post(post[0], post[1], username, post[3], post[4], post[5]))
        return posts

