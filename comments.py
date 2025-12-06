from dataclasses import dataclass

from query import query


@dataclass
class Comment:
    poster: str
    ts: str
    content: str
    commenter_id: int


def get_post_comments(post_id: int) -> list[Comment]:
    comment_tuples = query().select("ts, content, commenter_id")    \
                            .from_("Comments")                      \
                            .where("post_id = ?")                   \
                            .order_by("ts")                         \
                            .execute(post_id)                       \
                            .fetchall()

    comments = []
    for comment in comment_tuples:
        commenter = query().select("username")  \
                           .from_("Users")      \
                           .where("id = ?")     \
                           .execute(comment[2]) \
                           .fetchone()[0]
        comments.append(Comment(commenter, comment[0], comment[1], comment[2]))

    return comments


def add_comment(content, commenter_id, post_id) -> None:
    query().insert_into("Comments (content, commenter_id, post_id)")    \
           .values("(?, ?, ?)")                                         \
           .execute(content, commenter_id, post_id)

