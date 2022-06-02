-- file: create_tables.sql
-- Andrew Jarcho
-- 2022-05-30


DROP TABLE IF EXISTS tu_song CASCADE;

CREATE TABLE tu_song (
    song_id SERIAL UNIQUE,
    song_title varchar(120) NOT NULL,
    PRIMARY KEY (song_id),
    CONSTRAINT lowercase CHECK (song_title = lower(song_title))
);


DROP TABLE IF EXISTS tu_release CASCADE;

CREATE TABLE tu_release (
    release_id SERIAL UNIQUE,
    discogs_release_id bigint NOT NULL,
    discogs_release_string varchar(240) NOT NULL,
    PRIMARY KEY (release_id),
    CONSTRAINT lowercase CHECK (discogs_release_string = lower(discogs_release_string))
);


DROP TABLE IF EXISTS tu_song_release;

CREATE TABLE tu_song_release (
    song_release_id SERIAL UNIQUE,
    song_id integer NOT NULL,
    release_id integer NOT NULL,
    PRIMARY KEY (song_release_id),
    FOREIGN KEY (song_id) REFERENCES tu_song (song_id),
    FOREIGN KEY (release_id) REFERENCES tu_release (release_id)
);
