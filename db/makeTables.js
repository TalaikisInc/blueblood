const client = require('./conn')
const assert = require('assert')
assert.equal(typeof process.env.ENCODING_SECRET, 'string', 'You should set database encryption password')

const createTables = `
    CREATE TABLE IF NOT EXISTS blocks (
        block integer PRIMARY KEY
    );

    CREATE TABLE IF NOT EXISTS contracts (
        addr varchar(42) PRIMARY KEY,
        balance NUMERIC CHECK (balance > 0.5),
        byteCode text NOT NULL
    );

    CREATE TABLE IF NOT EXISTS addrs (
        addr varchar(42) PRIMARY KEY,
        balance NUMERIC CHECK (balance > 0.5)
    );

    CREATE SCHEMA IF NOT EXISTS basic_auth;

    CREATE TABLE IF NOT EXISTS basic_auth.users (
        email TEXT PRIMARY KEY CHECK (email ~* '^.+@.+\..+$'),
        pass TEXT NOT NULL CHECK (length(pass) < 512),
        role NAME NOT NULL CHECK (length(role) < 512),
        verified BOOLEAN NOT NULL DEFAULT false
    );

    DROP TYPE IF EXISTS token_type_enum CASCADE;
    CREATE TYPE token_type_enum AS enum ('validation', 'reset');

    CREATE TABLE IF NOT EXISTS basic_auth.tokens (
        token UUID PRIMARY KEY,
        token_type  token_type_enum NOT NULL,
        email TEXT NOT NULL REFERENCES basic_auth.users (email)
            ON DELETE CASCADE ON UPDATE CASCADE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT current_date
    );

    CREATE OR REPLACE FUNCTION
    basic_auth.check_role_exists() RETURNS trigger
        LANGUAGE plpgsql
        AS $$
    BEGIN
        if not exists (SELECT 1 FROM pg_roles as r WHERE r.rolname = new.role) THEN
            RAISE foreign_key_violation USING message =
                'unknown database role: ' || new.role;
            return null;
        end if;
        return new;
    END
    $$;

    DROP TRIGGER IF EXISTS ensure_user_role_exists on basic_auth.users;
    CREATE CONSTRAINT TRIGGER ensure_user_role_exists
        AFTER INSERT OR UPDATE ON basic_auth.users FOR EACH ROW
        EXECUTE PROCEDURE basic_auth.check_role_exists();
    
    CREATE EXTENSION IF NOT EXISTS pgcrypto;

    CREATE OR REPLACE FUNCTION
    basic_auth.encrypt_pass() RETURNS trigger
        LANGUAGE plpgsql
        AS $$
    BEGIN
        if tg_op = 'INSERT' or new.pass <> old.pass then
            new.pass = crypt(new.pass, gen_salt('bf'));
        end if;
        return new;
    END;
    $$;

    DROP TRIGGER IF EXISTS encrypt_pass ON basic_auth.users;
    CREATE TRIGGER encrypt_pass
        before insert or update ON basic_auth.users
        for each row
        EXECUTE PROCEDURE basic_auth.encrypt_pass();
    
    CREATE OR REPLACE FUNCTION
    basic_auth.user_role(email text, pass text) RETURNS name
        LANGUAGE plpgsql
        AS $$
    BEGIN
        return (
            SELECT role FROM basic_auth.users
                WHERE users.email = user_role.email
                AND users.pass = crypt(user_role.pass, users.pass)
        );
    END;
    $$;

    CREATE OR REPLACE FUNCTION
    login(email text, pass text) RETURNS basic_auth.tokens
        LANGUAGE plpgsql
        AS $$
    DECLARE
        _role name;
        _verified boolean;
        _email text;
        result basic_auth.tokens;
    BEGIN
        SELECT basic_auth.user_role(email, pass) INTO _role;
        if _role is null then
            RAISE invalid_password USING message = 'invalid user or password';
        end if;

        _email := email;
        SELECT verified FROM basic_auth.users AS u WHERE u.email=_email LIMIT 1 INTO _verified;
        IF NOT _verified THEN
            RAISE invalid_authorization_specification USING message = 'user is not verified';
        end if;

        SELECT sign(row_to_json(r), '${process.env.ENCODING_SECRET}') AS token
            FROM (
                SELECT _role AS role, login.email AS email,
                extract(epoch from now())::integer + 60*60 AS exp
            ) r
            INTO result;
        return result;
    END;
    $$;

    ALTER DATABASE ${process.env.PG_DB} SET postgrest.claims.email TO '';

    CREATE OR REPLACE FUNCTION
    basic_auth.current_email() RETURNS text
        LANGUAGE plpgsql
        AS $$
    BEGIN
        return current_setting('postgrest.claims.email');
    END;
    $$;

    CREATE ROLE anon;
    CREATE ROLE authenticator NOINHERIT;
    GRANT anon TO authenticator;

    GRANT USAGE ON SCHEMA public, basic_auth TO anon;
    GRANT SELECT ON TABLE pg_authid, basic_auth.users TO anon;
    GRANT EXECUTE ON FUNCTION login(text, text) TO anon;

    CREATE OR REPLACE FUNCTION
    request_password_reset(email text) RETURNS void
        LANGUAGE plpgsql
        AS $$
    DECLARE
        tok uuid;
    BEGIN
        DELETE FROM basic_auth.tokens
            WHERE token_type = 'reset'
        AND tokens.email = request_password_reset.email;

        SELECT gen_random_uuid() into tok;
        INSERT INTO basic_auth.tokens (token, token_type, email)
            VALUES (tok, 'reset', request_password_reset.email);
        PERFORM pg_notify('reset', json_build_object(
            'email', request_password_reset.email,
            'token', tok,
            'token_type', 'reset'
            )::text
        );
    END;
    $$;

    CREATE OR REPLACE FUNCTION
    reset_password(email text, token uuid, pass text)
        RETURNS void
        LANGUAGE plpgsql
        AS $$
    DECLARE
        tok uuid;
    BEGIN
        if exists(
            SELECT 1 FROM basic_auth.tokens
                WHERE tokens.email = reset_password.email
                AND tokens.token = reset_password.token
                AND token_type = 'reset') then
            UPDATE basic_auth.users set pass=reset_password.pass
                WHERE users.email = reset_password.email;
            DELETE FROM basic_auth.tokens
                WHERE tokens.email = reset_password.email
                AND tokens.token = reset_password.token
                AND token_type = 'reset';
        else
            RAISE invalid_password USING message = 'invalid user or token';
        end if;
        DELETE FROM basic_auth.tokens WHERE token_type = 'reset'
            AND tokens.email = reset_password.email;

        SELECT gen_random_uuid() into tok;
        INSERT INTO basic_auth.tokens (token, token_type, email)
            VALUES (tok, 'reset', reset_password.email);
        PERFORM pg_notify('reset', json_build_object(
            'email', reset_password.email,
            'token', tok
            )::text
        );
    END;
    $$;

    CREATE OR REPLACE FUNCTION
    basic_auth.send_validation() RETURNS trigger
        LANGUAGE plpgsql
        AS $$
    DECLARE
        tok uuid;
    BEGIN
        SELECT gen_random_uuid() INTO tok;
        INSERT INTO basic_auth.tokens (token, token_type, email)
            VALUES (tok, 'validation', new.email);
        PERFORM pg_notify('validate', json_build_object(
            'email', new.email,
            'token', tok,
            'token_type', 'validation'
            )::text
        );
        return new;
    END;
    $$;

    CREATE OR REPLACE VIEW users AS
    SELECT actual.role AS role,
        '***'::text AS pass,
        actual.email AS email,
        actual.verified AS verified
    FROM basic_auth.users AS actual,
        (SELECT rolname FROM pg_authid
        WHERE pg_has_role(current_user, oid, 'member')
        ) AS member_of
    WHERE actual.role = member_of.rolname;

    DROP TRIGGER IF EXISTS send_validation ON basic_auth.users;
    CREATE TRIGGER send_validation
        AFTER INSERT ON basic_auth.users
        FOR EACH ROW
        EXECUTE PROCEDURE basic_auth.send_validation();

    create or replace function
        basic_auth.clearance_for_role(u name) returns void as
        $$
        declare
          ok boolean;
        begin
          select exists (
            select rolname
              from pg_authid
             where pg_has_role(current_user, oid, 'member')
               and rolname = u
          ) into ok;
          if not ok then
            raise invalid_password using message =
              'current user not member of role ' || u;
          end if;
        end
        $$ LANGUAGE plpgsql;
        create or replace function
        update_users() returns trigger
        language plpgsql
        AS $$
        begin
          if tg_op = 'INSERT' then
            perform basic_auth.clearance_for_role(new.role);
        
            insert into basic_auth.users
              (role, pass, email, verified)
            values
              (new.role, new.pass, new.email,
              coalesce(new.verified, false));
            return new;
          elsif tg_op = 'UPDATE' then
            -- no need to check clearance for old.role because
            -- an ineligible row would not have been available to update (http 404)
            perform basic_auth.clearance_for_role(new.role);
        
            update basic_auth.users set
              email  = new.email,
              role   = new.role,
              pass   = new.pass,
              verified = coalesce(new.verified, old.verified, false)
              where email = old.email;
            return new;
          elsif tg_op = 'DELETE' then
            -- no need to check clearance for old.role (see previous case)
        
            delete from basic_auth.users
             where basic_auth.email = old.email;
            return null;
          end if;
        end
        $$;
        
        drop trigger if exists update_users on users;
        create trigger update_users
          instead of insert or update or delete on
            users for each row execute procedure update_users();

    create or replace function
signup(email text, pass text) returns void
as $$
  insert into basic_auth.users (email, pass, role) values
    (signup.email, signup.pass, 'hardcoded-role-here');
$$ language sql;
`

client.query(createTables, (err, res) => {
  console.log(err ? err.message : res)
  client.end()
})
