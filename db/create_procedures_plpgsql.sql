-- file create_procedures_plpgsql.sql
-- Andrew Jarcho
-- 2022-05-31


-- CREATE OR REPLACE FUNCTION tu_insert_song(new_song_title varchar) RETURNS text AS $$
-- DECLARE
--   tu_song_row tu_song%ROWTYPE;
-- 
-- BEGIN
--     SELECT * INTO tu_song_row FROM tu_song WHERE song_title = new_song_title;
-- 
--     IF FOUND THEN
--         RETURN 'tu_insert_song() failed: row already in table';
--     END IF;
-- 
--     INSERT INTO tu_song (song_id, song_title)
--     values (nextval('tu_song_song_id_seq'), new_song_title);
-- 
--     RETURN 'tu_insert_song() succeeded';
-- 
--     EXCEPTION
--         WHEN OTHERS THEN
--             RETURN 'error inserting song into db';
-- END;
-- $$ LANGUAGE plpgsql;
-- 
-- 
-- CREATE OR REPLACE FUNCTION tu_insert_release(new_discogs_release_id bigint, new_discogs_release_string varchar) RETURNS text AS $$
-- DECLARE
--     tu_release_row tu_release%ROWTYPE;
-- 
-- BEGIN
--     SELECT * INTO tu_release_row FROM tu_release WHERE release_id = new_discogs_release_id;
-- 
--     IF FOUND THEN
--         RETURN 'tu_insert_release() failed: row already in table';
--     END IF;
-- 
--     INSERT INTO tu_release (release_id, discogs_release_id, discogs_release_string)
--     values (nextval('tu_release_release_id_seq'), new_discogs_release_id, new_discogs_release_string);
-- 
--     RETURN 'tu_insert_release succeeded';
-- 
--     EXCEPTION
--         WHEN OTHERS THEN
--             RETURN 'error inserting release into db';
-- END;
-- $$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE tu_insert_all(
    new_discogs_release_id bigint, 
    new_discogs_release_string varchar,
    new_track_pos_str varchar, 
    new_track_title_str varchar, 
    new_track_duration_str varchar
) 
AS $$
DECLARE
    tu_song_row tu_song%ROWTYPE;
	tu_release_row tu_release%ROWTYPE;
    tu_song_id integer;
    tu_release_id integer;

BEGIN
	-- insert into the tu_song table
	INSERT INTO tu_song(song_title) 
	VALUES(new_track_title_str) 
	RETURNING song_id INTO tu_song_id;
	
	-- insert into the tu_release table
	INSERT INTO tu_release(discogs_release_id, discogs_release_string)
	VALUES(new_discogs_release_id, new_discogs_release_string)
	RETURNING release_id INTO tu_release_id;
	
	-- insert into vendor_parts
	INSERT INTO tu_song_release(song_id, release_id)
	VALUES(tu_song_id, tu_release_id);
	
END;
$$
LANGUAGE PLPGSQL;
