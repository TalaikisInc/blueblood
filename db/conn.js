const envLoc = process.env.NODE_ENV === 'production' ? '../.env' : '../.env.sample'
require('dotenv').config({ path: envLoc })

const { Client } = require('pg')

const client = new Client({
  user: process.env.PG_USER,
  host: process.env.PG_SERVER,
  database: process.env.PG_DB,
  password: process.env.PG_PASS,
  port: 5432
})

client.connect()

module.exports = client
