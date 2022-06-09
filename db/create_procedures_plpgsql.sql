-- file create_procedures_plpgsql.sql
-- Andrew Jarcho
-- 2022-05-31


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
    dummy_song tu_song%ROWTYPE;
    dummy_release tu_release%ROWTYPE;
    dummy_song_release tu_song_release%ROWTYPE;
BEGIN
    SELECT * INTO dummy_song FROM tu_song WHERE song_title = new_track_title_str;

    IF NOT FOUND THEN
	    -- insert into the tu_song table
	    INSERT INTO tu_song(song_title) 
	    VALUES(new_track_title_str) 
	    RETURNING song_id INTO tu_song_id;
    -- END IF;
    ELSE
        SELECT song_id INTO tu_song_id FROM tu_song WHERE tu_song.song_title = new_track_title_str;
    END IF;

        SELECT * INTO dummy_release FROM tu_release WHERE discogs_release_id = new_discogs_release_id;

        IF NOT FOUND THEN
	        -- insert into the tu_release table
	        INSERT INTO tu_release(discogs_release_id, discogs_release_string)
	        VALUES(new_discogs_release_id, new_discogs_release_string)
	        RETURNING release_id INTO tu_release_id;
        ELSE
            SELECT release_id INTO tu_release_id FROM tu_release WHERE discogs_release_id = new_discogs_release_id;
        END IF;
	
        SELECT * INTO dummy_song_release FROM tu_song_release WHERE song_id = tu_song_id AND release_id = tu_release_id;

        IF NOT FOUND THEN 
	        -- insert into tu_song_release table
	        INSERT INTO tu_song_release(song_id, release_id)
	        VALUES(tu_song_id, tu_release_id);
        END IF;
    -- END IF;
-- END IF;
END;
$$
LANGUAGE PLPGSQL;
