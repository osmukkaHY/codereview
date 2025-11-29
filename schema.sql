CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    ts TEXT DEFAULT (datetime('now')),
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY,
    ts TEXT DEFAULT (datetime('now')),
    poster_id INTEGER REFERENCES Users,
    title TEXT NOT NULL,
    context TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY,
    ts TEXT DEFAULT (datetime('now')),
    content TEXT NOT NULL,
    commenter_id INTEGER REFERENCES Users,
    post_id INTEGER REFERENCES Posts
);
