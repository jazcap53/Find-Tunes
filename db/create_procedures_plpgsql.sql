-- file create_procedures_plpgsql.sql
-- Andrew Jarcho
-- 2022-05-31


CREATE OR REPLACE FUNCTION tu_insert_person(new_person_name varchar,
    new_person_aka varchar) RETURNS text AS $$
DECLARE
  tu_person_row tu_person%ROWTYPE;

BEGIN
    SELECT * INTO tu_person_row FROM tu_person WHERE person_name = new_person_name AND
                                                   person_aka = new_person_aka;

    IF FOUND THEN
        RETURN 'tu_insert_person() failed: row already in table';
    END IF;

    INSERT INTO tu_person (person_id, person_name, person_aka)
    values (nextval('tu_person_person_id_seq'), new_person_name, new_person_aka);

    RETURN 'tu_insert_person() succeeded';

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'error inserting person into db';
END;
$$ LANGUAGE plpgsql;


-- CREATE OR REPLACE FUNCTION sl_insert_nap(new_start_time time without time zone,
--                                          new_duration interval hour to minute,
--                                          new_night_id integer)
--                                          RETURNS text AS $$
-- 
-- DECLARE
--     sl_nap_row sl_nap%ROWTYPE;
--     fk_night_id INTEGER;
-- 
-- BEGIN
--     SELECT * INTO sl_nap_row FROM sl_nap WHERE start_time = new_start_time AND
--                                                duration = new_duration AND
--                                                night_id = new_night_id;
-- 
--     IF FOUND THEN
--         RETURN 'sl_insert_nap() failed: row already in table';
--     END IF;
-- 
--     SELECT currval('sl_night_night_id_seq') INTO fk_night_id;
-- 
--     INSERT INTO sl_nap (nap_id, start_time, duration, night_id)
--     VALUES (nextval('sl_nap_nap_id_seq'), new_start_time, new_duration, fk_night_id);
--     RETURN 'sl_insert_nap() succeeded';
-- 
--     EXCEPTION
--         WHEN OTHERS THEN
--             RETURN 'error inserting nap into db';
-- 
-- END;
-- $$ LANGUAGE plpgsql;

