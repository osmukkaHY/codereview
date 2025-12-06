from dataclasses import dataclass

from db import execute, query as q
from query import query
import user


@dataclass
class Post:
    id:         str
    timestamp:  str
    poster_id:  int
    language:   str
    title:      str
    context:    str
    content:    str
    username:   str


class Posts:
    def __init__(self):
        pass

    def new(self,
            user_id: int,
            language: str,
            title: str,
            context: str,
            content: str) -> None:
        username = user.uname(user_id)
        execute("""
        INSERT INTO Posts
          (poster_id, lang, title, context, content, poster_username)
        VALUES
          (?, ?, ?, ?, ?, ?)
        """, user_id, language, title, context, content, username)


    def update(self,
            post_id: int,
            language: str,
            title: str,
            context: str,
            content: str) -> None:
        execute("""
        UPDATE Posts SET
          lang = ?, title = ?, context = ?, content = ?
        WHERE
          id = ?
        """, language, title, context, content, post_id)


    def by_id(self, id: int) -> Post | None:
        post = q("""
                 SELECT
                   id,
                   ts,
                   poster_id,
                   lang,
                   title,
                   context,
                   content,
                   poster_username
                 FROM
                   Posts
                 WHERE
                   id = ?
                 """, id)[0]

        if not post:
            return None

        return Post(post['id'],
                    post['ts'],
                    post['poster_id'],
                    post['lang'],
                    post['title'],
                    post['context'],
                    post['content'],
                    post['poster_username'])


    def n_recent(self, n: int):
        posts = q("""
                  SELECT
                    id, ts, poster_id, lang, title, context, content,
                    poster_username
                  FROM
                    Posts
                  ORDER BY
                    ts
                  LIMIT
                    ?
                  """, n)
        return [Post(post['id'],
                    post['ts'],
                    post['poster_id'],
                    post['lang'],
                    post['title'],
                    post['context'],
                    post['content'],
                    post['poster_username']) for post in posts]


    def by_user(self, user_id: str) -> list[Post]:
        posts = q("""
                  SELECT
                    id, ts, poster_id, lang, title, context, content,
                    poster_username
                  FROM
                    Posts
                  WHERE
                    poster_id = ?
                  ORDER BY
                    ts
                  """, user_id)
        return [Post(post['id'],
                    post['ts'],
                    post['poster_id'],
                    post['lang'],
                    post['title'],
                    post['context'],
                    post['content'],
                    post['poster_username']) for post in posts]


    def search(self, keyword: str, language: str) -> Post | None:
        posts = q("""
                  SELECT
                    id, ts, poster_id, lang, title, context, content,
                    poster_username
                  FROM
                    Posts
                  WHERE
                    content LIKE ? AND lang LIKE ?
                  """, '%'+keyword+'%', language)
        if not len(posts):
            return None
        
        return [Post(post['id'],
                    post['ts'],
                    post['poster_id'],
                    post['lang'],
                    post['title'],
                    post['context'],
                    post['content'],
                    post['poster_username']) for post in posts]
