-- file create_procedures_plpgsql.sql
-- Andrew Jarcho
-- 2022-05-31


CREATE OR REPLACE FUNCTION tu_insert_song(new_song_title varchar) RETURNS text AS $$
DECLARE
  tu_song_row tu_song%ROWTYPE;

BEGIN
    SELECT * INTO tu_song_row FROM tu_song WHERE song_title = new_song_title;

    IF FOUND THEN
        RETURN 'tu_insert_song() failed: row already in table';
    END IF;

    INSERT INTO tu_song (song_id, song_title)
    values (nextval('tu_song_song_id_seq'), new_song_title);

    RETURN 'tu_insert_song() succeeded';

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'error inserting song into db';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION tu_insert_release(new_discogs_release_id bigint, new_discogs_release_string varchar) RETURNS text AS $$
DECLARE
    tu_release_row tu_release%ROWTYPE;

BEGIN
    SELECT * INTO tu_release_row FROM tu_release WHERE release_id = new_release_id;

    IF FOUND THEN
        RETURN 'tu_insert_release() failed: row already in table';
    END IF;

    INSERT INTO tu_release (release_id, discogs_release_id, discogs_release_string)
    values (nextval('tu_release_release_id_seq'), new_discogs_release_id, new_discogs_release_string);

    RETURN 'tu_insert_release succeeded';

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'error inserting release into db';
END;
$$ LANGUAGE plpgsql;



