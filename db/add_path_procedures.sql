CREATE OR REPLACE PROCEDURE tu_insert_song_and_path(
song_title_str varchar,
song_path_str varchar)
AS $$
DECLARE
    tu_song_id integer;
    tu_path_id integer;
    song_row tu_song%ROWTYPE;
    path_row tu_path%ROWTYPE;
    dummy_song tu_song%ROWTYPE;
    dummy_path tu_path%ROWTYPE;
BEGIN
    SELECT * INTO dummy_song FROM tu_song WHERE song_title = song_title_str;

    IF NOT FOUND THEN
        -- insert into tu_song table
        INSERT INTO tu_song(song_title) 
        VALUES(song_title_str) 
        RETURNING tu_song.song_id INTO tu_song_id;
    ELSE
        tu_song_id = song_row.song_id;
    END IF;

    SELECT * INTO dummy_path FROM tu_path WHERE path = song_path_str;

    IF NOT FOUND THEN
        -- insert into tu_path table
        INSERT INTO tu_path(path)
        VALUES(song_path_str)
        RETURNING path_id INTO tu_path_id;
    ELSE
        tu_path_id = path_row.path_id;
    END IF;
    -- insert into tu_song_path table
    INSERT INTO tu_song_path(song_id, path_id)
    VALUES(tu_song_id, tu_path_id);
END;
$$
LANGUAGE PLPGSQL;
