const client = './conn'

const createTables = `
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";

    CREATE TABLE IF NOT EXISTS blocks (
        PRIMARY KEY block integer
    );

    CREATE TABLE IF NOT EXISTS contracts (
        PRIMARY KEY addr varchar(42),
        byteCode text
    );

    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        data JSONB
    );
`

await client.query(createTableText)
