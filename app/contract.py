import time
from logzero import logger
from web3 import Web3, HTTPProvider
from solc import compile_files

# Web3 setting
rpc_url = "http://localhost:8545"
w3 = Web3(HTTPProvider(rpc_url))
# w3 = Web3(IPCProvider("./chain-data/geth.ipc"))
w3.personal.unlockAccount(w3.eth.accounts[0], "test", 0)


def deploy(contract_file_name, contract_name):

    compiled_sol = compile_files([contract_file_name])
    interface = compiled_sol['{}:{}'.format(contract_file_name,
                                            contract_name)]

    contract = w3.eth.contract(abi=interface['abi'],
                               bytecode=interface['bin'],
                               bytecode_runtime=interface['bin-runtime'])

    # Deploy
    tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0]})

    logger.info("tx_hash: {}".format(tx_hash))

    # Mining
    w3.miner.start(2)
    time.sleep(5)
    w3.miner.stop()

    # Contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    logger.info("contract_address: {}".format(contract_address))
    # Use contract
    contract_instance = contract(contract_address)
    return contract_instance


def upload(ins, filehash, filename, filesize, owner):
    logger.info("Call upload")
    logger.info("{}, {}, {}, {}".format(owner, filehash, filename, filesize))
    transaction = ins.transact({"from": w3.eth.accounts[0]})
    tx_hash = transaction.upload(owner,
                                 filehash,
                                 filename,
                                 filesize)

    logger.info("Wait Uploading: {}".format(tx_hash))

    w3.miner.start(2)
    time.sleep(5)
    w3.miner.stop()

    logger.info("Finish Uploading")


def get_file_info(ins, filehash):
    logger.info("Call get_file_info")
    logger.debug(filehash)
    file_info = ins.call().getFileInfo(filehash)
    logger.debug(file_info)
    return file_info


def check_file_exist(ins, filehash):
    logger.info("Call check_file_exist")
    logger.debug(filehash)
    is_exist = ins.call().checkExist(filehash)
    logger.debug(is_exist)
    return is_exist
