CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY,
    ts DEFAULT TIMESTAMP
    poster_id INTEGER REFERENCES Users,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    ts DEFAULT TIMESTAMP,
    reviewer_id INTEGER REFERENCES Users,
    post_id INTEGER REFERENCES Posts,
    rating UNSIGNED TINYINT,
)
