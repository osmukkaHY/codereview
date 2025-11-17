from dataclasses import dataclass

from db import DB
from query import query


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
            user_id: str,
            title: str,
            context: str,
            content: str) -> None:
        query().insert_into('Posts (poster_id, title, context, content)')  \
               .values('(?, ?, ?, ?)')                                     \
               .execute(user_id, title, context, content)


    def by_id(self, id: int) -> Post | None:
        post_tuples = self._db.fetch("""SELECT *
                                       FROM Posts
                                       WHERE id = ?;""", id)
        print(post_tuples)
        if not len(post_tuples):
            return None
        post = post_tuples[0]
        username = self._db.fetch("""SELECT username
                                     FROM Users
                                     WHERE id = ?;""", post[2])[0][0]
        
        return Post(post[0], post[1], username, post[3], post[4], post[5])


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


    def search(self, keyword: str) -> Post | None:
        post_tuples = self._db.fetch("""SELECT *
                                        FROM Posts
                                        WHERE content LIKE ?""", '%'+keyword+'%')
        if not len(post_tuples):
            return None
        
        posts = []
        for post in post_tuples:
            username = self._db.fetch("""SELECT username
                                         FROM Users
                                         WHERE id = ?;""", post[2])[0][0]
            posts.append(Post(post[0], post[1], username, post[3], post[4], post[5]))
        return posts

