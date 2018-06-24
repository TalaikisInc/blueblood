const envLoc = process.env.NODE_ENV === 'production' ? '../.env' : '../.env.sample'
require('dotenv').config({ path: envLoc })
const { Client } = require('pg')
const client = new Client({
  user: process.env.PG_USER,
  host: process.env.PG_SERVER,
  database: process.env.PG_DB,
  password: process.env.PG_PASS,
  port: 3211
})

const conn = await client.connect()

export default conn
