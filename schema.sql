CREATE TABLE visits (id INTEGER PRIMARY KEY, visited_at TEXT);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE workout_types (
    workout_type TEXT PRIMARY KEY
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    content TEXT,
    posted_at TEXT,
    workout_type TEXT REFERENCES workout_types,
    title TEXT
);