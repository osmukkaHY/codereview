from db import execute, query
import user


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
          (poster_id, language, title, context, content, poster_username)
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
        post = query("""
                 SELECT id, timestamp, poster_id, language, title, context,
                        content, poster_username
                 FROM
                   Posts
                 WHERE
                   id = ?
                 """, id)[0]
        return post


    def n_recent(self, n: int):
        posts = query("""
                  SELECT
                    id, timestamp, poster_id, language, title, context, content,
                    poster_username
                  FROM
                    Posts
                  ORDER BY
                    timestamp
                  LIMIT
                    ?
                  """, n)
        return posts

    def by_user(self, user_id: str) -> list[Post]:
        posts = query("""
                  SELECT
                    id, timestamp, poster_id, language, title, context, content,
                    poster_username
                  FROM
                    Posts
                  WHERE
                    poster_id = ?
                  ORDER BY
                    timestamp
                  """, user_id)
        return posts

    def search(self, keyword: str, language: str) -> Post | None:
        posts = query("""
                  SELECT
                    id, timestamp, poster_id, language, title, context, content,
                    poster_username
                  FROM
                    Posts
                  WHERE
                    content LIKE ? AND language LIKE ?
                  """, '%'+keyword+'%', language)
        return posts
