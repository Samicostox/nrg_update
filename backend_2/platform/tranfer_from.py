

import json
import os
from web3 import Web3


_to = Web3.toChecksumAddress("0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1")
_from = Web3.toChecksumAddress("0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0")
_amount = 400
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
with open('api/assets/NRGToken.json', 'r') as file:
  nrgJson = json.load(file)
abi = nrgJson["abi"]
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")
contractAddress = Web3.toChecksumAddress('0xe78a0f7e598cc8b0bb87894b0f60dd2a88d6a8ab')

nonce = w3.eth.getTransactionCount(my_address)
nrg_token = w3.eth.contract(address=contractAddress, abi=abi)
estimate = w3.eth.estimate_gas({"from":"0x8D97689C9818892B700e27F316cc3E41e17fBeb9","to":"0xd3CdA913deB6f67967B99D67aCDFa1712C293601","value":"0x186a0"})
print(estimate)
store_transaction = nrg_token.functions.transferFrom(_from, _to, int(_amount)).buildTransaction(
{"chainId": chain_id, "from":my_address, "nonce":nonce, "gas":2100000}
)
nonce +=1
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(nrg_token.functions.getBalance(my_address).call())