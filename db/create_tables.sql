-- file: create_tables.sql
-- Andrew Jarcho
-- 2022-05-30


DROP TABLE IF EXISTS tu_person CASCADE;

CREATE TABLE tu_person (
    person_id SERIAL UNIQUE,
    name varchar(120) NOT NULL,
    aka varchar(120),
    PRIMARY KEY (person_id)
);


DROP TABLE IF EXISTS tu_action CASCADE;

CREATE TABLE tu_action (
    action_id SERIAL UNIQUE,
    did_what varchar(120) NOT NULL,
    PRIMARY KEY (action_id)
);


DROP TABLE IF EXISTS tu_person_action;

CREATE TABLE tu_person_action (
    person_action_id SERIAL UNIQUE,
    person_id integer NOT NULL,
    action_id integer NOT NULL,
    PRIMARY KEY (person_action_id),
    FOREIGN KEY (person_id) REFERENCES tu_person (person_id),
    FOREIGN KEY (action_id) REFERENCES tu_action (action_id)
);


DROP TABLE IF EXISTS tu_song CASCADE;

CREATE TABLE tu_song (
    song_id SERIAL UNIQUE,
    song_title varchar(120) NOT NULL,
    PRIMARY KEY (song_id)
);


DROP TABLE IF EXISTS tu_release CASCADE;

CREATE TABLE tu_release (
    release_id SERIAL UNIQUE,
    release_title varchar(120) NOT NULL,
    PRIMARY KEY (release_id)
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
