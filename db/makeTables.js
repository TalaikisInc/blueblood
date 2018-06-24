const client = require('./conn')

const createTables = `
    CREATE TABLE IF NOT EXISTS blocks (
        block integer PRIMARY KEY
    );

    CREATE TABLE IF NOT EXISTS contracts (
        addr varchar(42) PRIMARY KEY,
        byteCode text
    );
`

client.query(createTables, (err, res) => {
  console.log(err ? err.message : res)
  client.end()
})
