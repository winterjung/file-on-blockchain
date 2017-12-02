# File on blockchain

## Initialize blockchain environment
1. `git clone https://github.com/JungWinter/file-on-blockchain`
2. `cd file-on-blockchain/blockchain`
3. `./init.sh`
4. `./start.sh`

## Create account for deploying
1. Open another terminal and move to `file-on-blockchain/blockchain`
2. `geth attach ./chain-data/geth.ipc`
3. In console, `personal.newAccount()` and enter password
4. `miner.start()` and `miner.stop()`

## Deploy simple contract
1. `cd file-on-blockchain/example`
2. `python deploy_contract_and_test.py`
3. :tada:

## Run server
1. `cd file-on-blockchain/app`
2. `python server.py`
3. :star:
