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


CREATE OR REPLACE FUNCTION tu_insert_action(new_did_what varchar) RETURNS text AS $$
DECLARE
    tu_action_row tu_action%ROWTYPE;

BEGIN
    SELECT * INTO tu_action_row FROM tu_action WHERE did_what = new_did_what;

    IF FOUND THEN
        RETURN 'tu_insert_action() failed: row already in table';
    END IF;

    INSERT INTO tu_action (action_id, did_what)
    values (nextval('tu_action_action_id_seq'), new_did_what);

    RETURN 'tu_insert_action succeeded';

    EXCEPTION
        WHEN OTHERS THEN
            RETURN 'error inserting action into db';
END;
$$ LANGUAGE plpgsql;
