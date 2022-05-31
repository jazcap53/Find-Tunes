-- file: create_tables.sql
-- Andrew Jarcho
-- 2022-05-30


DROP TABLE IF EXISTS tu_person CASCADE;

CREATE TABLE tu_person (
    person_id SERIAL UNIQUE,
    person_name varchar(120) NOT NULL,
    person_aka varchar(120),
    PRIMARY KEY (person_id),
    CONSTRAINT lowercase CHECK (person_name = lower(person_name) AND person_aka = lower(person_aka))
);


DROP TABLE IF EXISTS tu_action CASCADE;

CREATE TABLE tu_action (
    action_id SERIAL UNIQUE,
    did_what varchar(120) NOT NULL,
    PRIMARY KEY (action_id),
    CONSTRAINT lowercase CHECK (did_what = lower(did_what))
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
    PRIMARY KEY (song_id),
    CONSTRAINT lowercase CHECK (song_title = lower(song_title))
);


DROP TABLE IF EXISTS tu_release CASCADE;

CREATE TABLE tu_release (
    release_id SERIAL UNIQUE,
    release_title varchar(120) NOT NULL,
    PRIMARY KEY (release_id),
    CONSTRAINT lowercase CHECK (release_title = lower(release_title))
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


DROP TABLE IF EXISTS tu_person_release;

CREATE TABLE tu_person_release (
    person_release_id SERIAL UNIQUE,
    person_id integer NOT NULL,
    release_id integer NOT NULL,
    PRIMARY KEY (person_release_id),
    FOREIGN KEY (person_id) REFERENCES tu_person (person_id),
    FOREIGN KEY (release_id) REFERENCES tu_release (release_id)
);
