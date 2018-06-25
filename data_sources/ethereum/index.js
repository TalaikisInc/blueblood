const envLoc = process.env.NODE_ENV === 'production' ? '../../.env' : '../../.env.sample'
require('dotenv').config({ path: envLoc })
const Web3 = require('web3')
const web3 = new Web3(new Web3.providers.HttpProvider(`https://mainnet.infura.io/${process.env.INFURA_API_KEY}`))
const client = require('../../db/conn')
const chalk = require('chalk')

let blockNum = 0
client.query('SELECT block FROM blocks ORDER BY block DESC LIMIT 1', (err, res) => {
  if (!err) {
    blockNum = res.rows[0] ? res.rows[0].block : 0
  } else {
    console.log(chalk.red(err.message))
  }
})

const getBalance = async (client, tx) => {
  await web3.eth.getBalance(tx.to, (err, balance) => {
    if (!err) {
      client.query('INSERT INTO addrs(addr, balance) VALUES($1, $2)', [tx.to, balance], (err, res) => {
        console.log(err ? chalk.red(err.message) : chalk.green(`Addr: ${tx.to}`))
      })
    } else {
      console.log(chalk.red(err.message))
    }
  })
  return balance
}

const getCodes = async (client, balance, tx) => {
  await web3.eth.getCode(tx.to, (err, code) => {
    if (!err) {
      client.query('INSERT INTO contracts(addr, balance, byteCode) VALUES($1, $2, $3)', [tx.to, balance, code], (err, res) => {
        console.log(err ? chalk.red(err.message) : chalk.green(`Block: ${blck}`))
      })
    } else {
      console.log(chalk.red(err.message))
    }
  })
}

const collect = async () => {
  while (true) {
    let blck = blockNum++
    let block = await web3.eth.getBlock(blck)
    if (!block) {
      break
    }

    for(let i = 0; i < block.transactions.length; i++) {
      let tx = await web3.eth.getTransaction(block.transactions[i])
      if (parseInt(tx.value) > 0) {
        const balance = await getBalance(client, tx)
        await getCodes(client, balance, tx)
      }
    }

    client.query('INSERT INTO blocks(block) VALUES($1)', [blck], (err, res) => {
      console.log(err ? chalk.red(err.message) : chalk.green(`Block: ${blck}`))
    })
  }

  client.end()
}

collect()
