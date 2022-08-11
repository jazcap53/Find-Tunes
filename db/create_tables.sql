-- file: create_tables.sql
-- Andrew Jarcho
-- 2022-05-30


DROP TABLE IF EXISTS tu_song CASCADE;

CREATE TABLE tu_song (
    song_id SERIAL UNIQUE,
    song_title text NOT NULL UNIQUE,
    PRIMARY KEY (song_id),
    CONSTRAINT lowercase CHECK (song_title = lower(song_title))  -- ,
    -- CONSTRAINT not_both_null CHECK (tu_song_release.release_id is not null or tu_song_path.path_id is not null)
);


DROP TABLE IF EXISTS tu_release CASCADE;

CREATE TABLE tu_release (
    release_id SERIAL UNIQUE,
    discogs_release_id bigint,
    release_string text NOT NULL,
    PRIMARY KEY (release_id),
    CONSTRAINT lowercase CHECK (release_string = lower(release_string))
);


DROP TABLE IF EXISTS tu_song_release;

CREATE TABLE tu_song_release (
    song_release_id SERIAL UNIQUE,
    song_id integer NOT NULL REFERENCES tu_song (song_id) ON DELETE CASCADE,
    release_id integer REFERENCES tu_release (release_id) ON DELETE CASCADE,
    PRIMARY KEY (song_release_id)
);

/*
DROP TABLE IF EXISTS tu_path;

CREATE TABLE tu_path (
    path_id integer NOT NULL,
    path_string varchar(240) NOT NULL UNIQUE,
    PRIMARY KEY (path_id),
    CONSTRAINT lowercase CHECK (path_string = lower(path_string))
);


DROP TABLE IF EXISTS tu_song_path;

CREATE TABLE tu_song_path (
    song_path_id SERIAL UNIQUE,
    song_id integer NOT NULL REFERENCES tu_song (song_id) ON DELETE CASCADE,
    path_id integer REFERENCES tu_path (path_id) ON DELETE CASCADE,
    PRIMARY KEY (song_path_id)
);
*/
