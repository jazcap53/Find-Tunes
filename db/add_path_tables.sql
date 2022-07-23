DROP TABLE IF EXISTS tu_path CASCADE;

CREATE TABLE tu_path (
    path_id SERIAL,
    path varchar(240) NOT NULL,
    PRIMARY KEY (path_id)
);

DROP TABLE IF EXISTS tu_song_path;

CREATE TABLE tu_song_path (
    song_path_id SERIAL,
    song_id integer NOT NULL REFERENCES tu_song (song_id) ON DELETE CASCADE,
    path_id integer NOT NULL REFERENCES tu_path (path_id) ON DELETE CASCADE,
    PRIMARY KEY (song_path_id)
);
