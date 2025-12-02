from dataclasses import dataclass

from db import DB
from query import query


@dataclass
class Post:
    id:         str
    timestamp:  str
    username:   str
    language:   str
    title:      str
    context:    str
    content:    str


class Posts:
    def __init__(self):
        self._db = DB()


    def new(self,
            user_id: int,
            language: str,
            title: str,
            context: str,
            content: str) -> None:
        query().insert_into('Posts (poster_id, lang, title, context, content)')  \
               .values('(?, ?, ?, ?, ?)')                                     \
               .execute(user_id, language, title, context, content)


    def update(self,
            post_id: str,
            language: str,
            title: str,
            context: str,
            content: str) -> None:
        query().update('Posts')                             \
               .set("lang = ?, title = ?, context = ?, content = ?")  \
               .where("id = ?")                             \
               .execute(language, title, context, content, post_id)


    def by_id(self, id: int) -> Post | None:
        post = query().select('id, ts, poster_id, lang, title, context, content')  \
                             .from_('posts')                                        \
                             .where('id = ?')                                       \
                             .execute(id)                                           \
                             .fetchone()
        if not post:
            return None

        username = query().select('username')   \
                          .from_('Users')       \
                          .where('id = ?')      \
                          .execute(post[2])     \
                          .fetchone()[0]
        if not username:
            return None

        return Post(post[0], post[1], username, post[3], post[4], post[5], post[6])


    def n_recent(self, n: int):
        post_tuples = query().select('id, ts, poster_id, lang, title, context, content') \
                       .from_('Posts')                                      \
                       .order_by('ts')                                      \
                       .limit('?')                                          \
                       .execute(n)                                           \
                       .fetchall()
        username = lambda id: query().select('username')  \
                                     .from_('Users')      \
                                     .where('id = ?')     \
                                     .execute(id)         \
                                     .fetchone()[0]
        return [Post(post[0],
                     post[1],
                     username(post[2]),
                     post[3],
                     post[4],
                     post[5],
                     post[6]) for post in post_tuples]


    def by_user(self, user_id: str) -> list[Post]:
        post_tuples = query().select('id, ts, poster_id, lang, title, context, content')  \
                             .from_('Posts')                                        \
                             .where('poster_id = ?')                                \
                             .order_by('ts')                                        \
                             .execute(user_id)                                      \
                             .fetchall()
        username = lambda id: query().select('username')  \
                                     .from_('Users')      \
                                     .where('id = ?')     \
                                     .execute(id)         \
                                     .fetchone()[0]
        return [Post(post[0],
                     post[1],
                     username(post[2]),
                     post[3],
                     post[4],
                     post[5],
                     post[6]) for post in post_tuples]


    def search(self, keyword: str, language: str) -> Post | None:
        post_tuples = query().select('id, ts, poster_id, lang, title, context, content')  \
                             .from_('Posts')                                        \
                             .where('content LIKE ?' + ' AND lang LIKE ?')             \
                             .execute('%'+keyword+'%', language)                              \
                             .fetchall()
        if not len(post_tuples):
            return None
        
        username = lambda id: query().select('username')  \
                                     .from_('Users')      \
                                     .where('id = ?')     \
                                     .execute(id)         \
                                     .fetchone()[0]
        return [Post(post[0],
                     post[1],
                     username(post[2]),
                     post[3],
                     post[4],
                     post[5],
                     post[6]) for post in post_tuples]
