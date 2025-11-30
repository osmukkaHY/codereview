from dataclasses import dataclass


@dataclass
class Profile:
    username: str
    post_count: int
    join_date: str
