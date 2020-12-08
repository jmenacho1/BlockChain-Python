# Set imports
import subprocess
import json
from json.decoder import JSONDecodeError
from constants import *
from web3 import Web3
import os
from dotenv import load_dotenv
from eth_account import Account
from pathlib import Path
from bit import wif_to_key, PrivateKeyTestnet, PrivateKey, Key
from getpass import getpass


#from constants import BTC,BTCTEST,ETH




load_dotenv()

# Set env to call mnemonic
mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here')

#Let's make a connection with Web3
#w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER',"http://localhost:8545")))



'''
OLD STUFF = CAN DELETE // no f (format)
def derive_wallets(mnemonic, coin, numderive):
    """Use the subprocess library to call the php file script from Python"""
    command  = 'php hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --numderive="{numderive}" --coin="{coin}" --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    # read data from standard output and err
    (output, err) = p.communicate()
    # Need to wait for child process to terminate - allows you to run process. 
    p_status = p.wait()
    keys = json.loads(output)
    return keys
'''


def derive_wallets(coin=BTC,mnemonic=mnemonic,depth=3):
    command = f"php hd-wallet-derive/hd-wallet-derive.php -g --mnemonic='{mnemonic}' --coin={coin} --numderive={depth} --format=json"
    p = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    (output,err) = p.communicate()
    p_status = p.wait()
    '''Get a Json Decoder issue. Tried the following two with not success:'''
    #output2 = str(output).strip("'<>() ").replace('\'','\"')
    #output2 = output.decode("utf-8")[0]
    return json.loads(output)

# Add to function 
coins = ["eth", "btc-test", "btc"]
numderive=3


# Call the function iterating through the coins using dict comprehension
{coin: derive_wallets(os.getenv('mnemonic'), coin, numderive) for coin in coins}



'''
def create_tx(coin, account, to, amount):
    if coin == ETH:
        #Convert ETH to Wei
        value = w3.toWei(amount, "ether") 
        gasEstimate = w3.eth.estimateGas({ "to": to, "from": account.address, "amount": value })
        return {
            "to": to,
            "from": account.address,
            "value": value,
            "gas": gasEstimate,
            "gasPrice": w3.eth.generateGasPrice(),
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainId": w3.net.chainId
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])


def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    if coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)






# Add to function 
numderive=3
finalOutput = {ETH:derive_wallets(coin=ETH), BTCTEST: derive_wallets(coin=BTCTEST)}
print(finalOutput)

'''