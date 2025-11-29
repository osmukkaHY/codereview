from dataclasses import dataclass

from query import query


@dataclass
class Comment:
    poster: str
    text: str


def get_post_comments(post_id) -> 
