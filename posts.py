from sqlite3 import Row
from db import execute, query
import user


def new(user_id:   int,
        language:  str,
        title:     str,
        context:   str,
        content:   str) -> None:
    username = user.uname(user_id)
    execute("""
            INSERT INTO Posts
              (poster_id, language, title, context, content, poster_username)
            VALUES
              (?, ?, ?, ?, ?, ?)
            """, user_id, language, title, context, content, username)


def update(post_id:    int,
            language:  str,
            title:     str,
            context:   str,
            content:   str) -> None:
    execute("""
            UPDATE Posts SET
              lang = ?, title = ?, context = ?, content = ?
            WHERE
              id = ?
            """, language, title, context, content, post_id)


def by_id(id: int) -> Row:
    return query("""
                 SELECT id, timestamp, poster_id, language, title, context,
                        content, poster_username
                 FROM
                   Posts
                 WHERE
                   id = ?
                 """, id)[0]


def n_recent(n: int) -> Row:
    return query("""
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


def by_user(user_id: str) -> Row:
    return query("""
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


def search(keyword: str, language: str) -> Row:
    return query("""
                 SELECT
                   id, timestamp, poster_id, language, title, context, content,
                   poster_username
                 FROM
                   Posts
                 WHERE
                   content LIKE ? AND language LIKE ?
                 """, '%'+keyword+'%', language)
