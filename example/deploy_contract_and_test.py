import time
from web3 import Web3, HTTPProvider
from solc import compile_source

# Code
contract_source_code = '''
contract Greeter {
    string public greeting;

    function Greeter() {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() constant returns (string) {
        return greeting;
    }
}
'''

# Web3 setting
rpc_url = "http://localhost:8545"
w3 = Web3(HTTPProvider(rpc_url))
# w3 = Web3(IPCProvider("./chain-data/geth.ipc"))
w3.personal.unlockAccount(w3.eth.accounts[0], "test", 0)


# Compile
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Greeter']

contract = w3.eth.contract(abi=contract_interface['abi'],
                           bytecode=contract_interface['bin'],
                           bytecode_runtime=contract_interface['bin-runtime'])

# Deploy
tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0]})

print("tx_hash: {}".format(tx_hash))
print("Finish deploying")

# Mining
w3.miner.start(2)
time.sleep(5)
w3.miner.stop()

# Contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
contract_address = tx_receipt['contractAddress']

# Use contract
contract_instance = contract(contract_address)
# Get
print('Contract value: {}'.format(contract_instance.call().greet()))
# Set
contract_instance.transact({"from": w3.eth.accounts[0]}).setGreeting("WinterJ")
print('Setting value to: WinterJ')

# Mining
w3.miner.start(2)
time.sleep(5)
w3.miner.stop()

# Get
print('Contract value: {}'.format(contract_instance.call().greet()))
