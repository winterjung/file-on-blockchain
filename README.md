# File on blockchain

|Index    |Upload result|File info|
|:-------:|:-----------:|:-------:|
|![upload]|![result]    |![info]  |


|Check   |Exist  |None    |
|:------:|:-----:|:------:|
|![check]|![true]|![false]|



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


[upload]: https://raw.githubusercontent.com/JungWinter/JungWinter.github.io/master/images/20171203/02_upload_file.png
[result]: https://raw.githubusercontent.com/JungWinter/JungWinter.github.io/master/images/20171203/03_upload_result.png
[info]: https://raw.githubusercontent.com/JungWinter/JungWinter.github.io/master/images/20171203/04_info.png
[check]:https://raw.githubusercontent.com/JungWinter/JungWinter.github.io/master/images/20171203/05_check.png
[true]:https://raw.githubusercontent.com/JungWinter/JungWinter.github.io/master/images/20171203/06_true.png
[false]: https://raw.githubusercontent.com/JungWinter/JungWinter.github.io/master/images/20171203/08_false.png
