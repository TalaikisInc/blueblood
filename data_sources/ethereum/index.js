const Web3 = require('web3')
const web3 = new Web3(new Web3.providers.HttpProvider(`https://mainnet.infura.io/${process.env.INFURA_API_KEY}`))
const client = '../db/conn'

let blockNum = 0
const collectContracts = async () => {
  while (true) {
    let blck = blockNum++
    let block = await web3.eth.getBlock(blck)
    if (!block) {
      break
    }

    for(let i = 0; i < block.transactions.length; i++) {
      let tx = await web3.eth.getTransaction(block.transactions[i])
      if (parseInt(tx.value) > 0) {
        await web3.eth.getCode(tx.to, (code, err) => {
            if (code) {
              await client.query('INSERT INTO contracts(id, addr, byteCode) VALUES(NULL, $1, $2)', [tx.to, code]).catch((e) => {
                console.log(e)
              })
            }
        })
      }
    }

    await client.query('INSERT INTO blocks(block) VALUES($1)', [blck]).catch((e) => {
      console.log(e)
    })
  }

  await client.end()
}

collectContracts()
