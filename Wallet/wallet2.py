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




load_dotenv()

# Set env to call mnemonic
mnemonic = os.getenv('mnemonic')



def derive_wallets(mnemonic, coin, numderive):
    """Use the subprocess library to call the php file script from Python"""
    command = f'php hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --numderive="{numderive}" --coin="{coin}" --format=json'
    # ^ i think if u have ' after f then i think you have to have " around the variables u are passing thru. same as if u had " with the f to start - u wud have to have ' around the variables u are passing thru

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    # read data from standard output and err
    (output, err) = p.communicate()
    # Need to wait for child process to terminate - allows you to run process. 
    p_status = p.wait()
    '''Got a Json Decoder issue. Tried the following two with not success:'''
    #output2 = str(output).strip("'<>() ").replace('\'','\"')
    #output2 = output.decode("utf-8")[0]
    keys = json.loads(output)
    return  keys
    

# Add to function 
coins = ["eth", "btc-test", "btc"]
numderive=3





keys = {}
for coin in coins:
    keys[coin]= derive_wallets(os.getenv('mnemonic'), coin, numderive)



# print(keys)  # u can also run this is output it in a different format:   print(json.dumps(keys, indent=4, sort_keys=True))

# Need address to prefund an account on the BTC Transaction Below

# print(keys['eth'][0]['address'])

# Need address to prefund an account on the BTC Transaction Below

# print(keys['btc-test'][0]['address'])


# print(keys['btc-test'][0]['privkey'])


#Activate w3 for Ether Transactions
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


eth_privatekey = keys['eth'][0]['privkey']
btc_privatekey = keys['btc-test'][0]['privkey']    ## might want to change the name of second object to btc-test_privatekey

# print(json.dumps(eth_privatekey, indent=4, sort_keys=True))
# print(json.dumps(btc_privatekey, indent=4, sort_keys=True))


# Create Function 1 of 3
def priv_key_to_account(coin, priv_key):
    '''Convert the privkey string in a child key to an account object that bit or web3.py can use'''
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
eth_account = priv_key_to_account(ETH,eth_privatekey)
btc_account = priv_key_to_account(BTCTEST,btc_privatekey)




# Create Function 2 of 3
def create_tx(coin, account, recipient, amount):
    """create the raw, unsigned transaction that contains all metadata needed to transact"""
    if coin ==ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount})
        return{
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])



# Create Function 3 of 3
def send_tx(coin, account, recipient, amount):
    """call create_trx, sign the transaction, then send it to the designated network"""
    if coin =='eth':
        txn = create_tx(coin, account, recipient, amount)
        signed_txn = w3.eth.account.signTransaction(txn)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(result.hex())
        return result.hex()

    else:
        tx_btctest= create_tx(coin, account, recipient, amount)
        sign_tx_btctest = account.sign_transaction(tx_btctest)
        from bit.network import NetworkAPI
        NetworkAPI.broadcast_tx_testnet(sign_tx_btctest)       
        return sign_tx_btctest







# Set up Priv Keys for Transacting Ether and BTC test Accounts
# print(eth_account)
# print(btc_account)



# Get Regenerated Keys for BTC Test        ## i had to input the priv key for index=0, btc-test below:
print(priv_key_to_account('btc-test', 'cVLWzzgcjU9KdC3tPQT86mRHKxeRCkMXmWSA4E6Kd4VY4U51NnFJ'))

## outputs the address for the above: mjrcFmdbSj2TkRpjCMQV1SE2Yrfe9dyvo4



#########  Generating Tranactions in BTC   ################



## Create Transaction in BTC Test - 

print(create_tx('btc-test',btc_account, 'mjrcFmdbSj2TkRpjCMQV1SE2Yrfe9dyvo4', .0001))


# Send Transaction - 
print(send_tx('btc-test',btc_account,'mjrcFmdbSj2TkRpjCMQV1SE2Yrfe9dyvo4',0.000001))



# Create Transaction in BTC Test - Send Back To Test Net
print(create_tx('btc-test',btc_account, 'mjrcFmdbSj2TkRpjCMQV1SE2Yrfe9dyvo4', 0.01))



## Generating Transactions in ETHER

from web3.middleware import geth_poa_middleware
#w3.middleware_onion.inject(geth_poa_middleware, layer=0)

private_key = os.getenv("Private_Key")
print(keys['eth'][0]['privkey'])
print(keys['eth'][0]['address'])
#w3.eth.blockNumber
with open(
    Path("UTC--2020-10-31T12-43-11.018Z--5118a4a79e780824c1a6b5d98ebfcbaaa3876de2")
)as keyfile:
    encrypted_key = keyfile.read()
    private_key = w3.eth.account.decrypt(encrypted_key, getpass("Enter keystore password: "))

''' ^ i used the keystore from my "vaultone" network from mycrypto from the last homework: BlockChain ^ '''

from web3 import Web3, HTTPProvider
#w3.eth.blockNumber

# Get Regenerated Key for ETHER (eth [0] priv key:)
priv_key_to_account('eth', '0xf875883bccb5a382c5271c646d76f1d4d9593777d39fae0c444fce3670bbc05e')

# Create Transaction in ETHER - problem funding the account  (eth [0] address key:)
create_tx(ETH,eth_account, '0xD4D5B6A7E306747A7aFefB291c387a03DC0CBa6A', 1.0)


# Send Transaction in ETHER - problem funding the account   (eth [0] address key:)
create_tx(ETH,eth_account, '0xD4D5B6A7E306747A7aFefB291c387a03DC0CBa6A', 1.0)


