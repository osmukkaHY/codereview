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
        print(type(post))

        return Post(post['id'],
                    post['ts'],
                    post['poster_id'],
                    post['lang'],
                    post['title'],
                    post['context'],
                    post['content'],
                    post['poster_username'])


    def n_recent(self, n: int):
        post_tuples = query().select('id, ts, poster_id, lang, title, context, content, poster_username') \
                       .from_('Posts')                                      \
                       .order_by('ts')                                      \
                       .limit('?')                                          \
                       .execute(n)                                           \
                       .fetchall()
        return [Post(post[0],
                     post[1],
                     post[2],
                     post[3],
                     post[4],
                     post[5],
                     post[6],
                     post[7]) for post in post_tuples]


    def by_user(self, user_id: str) -> list[Post]:
        post_tuples = query().select('id, ts, poster_id, lang, title, context, content, poster_username')  \
                             .from_('Posts')                                        \
                             .where('poster_id = ?')                                \
                             .order_by('ts')                                        \
                             .execute(user_id)                                      \
                             .fetchall()
        return [Post(post[0],
                     post[1],
                     post[2],
                     post[3],
                     post[4],
                     post[5],
                     post[6],
                     post[7]) for post in post_tuples]


    def search(self, keyword: str, language: str) -> Post | None:
        post_tuples = query().select('id, ts, poster_id, lang, title, context, content, poster_username')  \
                             .from_('Posts')                                        \
                             .where('content LIKE ?' + ' AND lang LIKE ?')             \
                             .execute('%'+keyword+'%', language)                              \
                             .fetchall()
        if not len(post_tuples):
            return None
        
        return [Post(post[0],
                     post[1],
                     post[2],
                     post[3],
                     post[4],
                     post[5],
                     post[6],
                     post[7]) for post in post_tuples]
