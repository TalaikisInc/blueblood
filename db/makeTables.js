const client = require('./conn')

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
`

client.query(createTables, (err, res) => {
  console.log(err ? err.message : res)
  client.end()
})
