import requests
from eth_account import Account
import json
from mnemonic import Mnemonic
import bip32utils

def append_to_json(file_path, data):
    # Step 1: Load existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Step 2: Modify the loaded data by appending new data
    existing_data.append(data)

    # Step 3: Write the modified data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file)

# File path of the JSON file
file_path = 'E:\Python Workspace\crypto\data.json'


def check_transactions(address):
    # Replace 'YOUR_API_KEY' with your Etherscan API key
    api_eth = '7WKM5ZPIIM5MRNRHQA5HDFTSBP23HUS4JJ'
    # Construct the API endpoint URL
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_eth}"

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if any transactions were found
        if data['status'] == '1' and data['message'] == 'OK' and len(data['result']) > 0:
            print(f"The address '{address}' has transactions.")
            print(phrase)
            new_data = {"phrase": phrase, "address": address, "chain": "ETH"}
            append_to_json(file_path, new_data)
        else:
            pass
            #print(f"The address '{address}' has no transactions.")
    else:
        print("Error occurred while retrieving transaction data.")


def check_address_transactions(address):
    api_bsc= "TYSVVF3AXE45TXJ9DAX9KDYSSEP4JCRBGS"
    api_url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_bsc}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data["status"] == "1":
            transactions = data["result"]
            if len(transactions) > 0:
                print(f"The address {address} has {len(transactions)} transactions.")
                print(phrase)
                new_data = {"phrase": phrase, "address": address, "chain": "BSC"}
                append_to_json(file_path, new_data)
            else:
                print(f"The address {address} has no transactions.")
        else:
            pass
            #print("API request failed.")
            #if "message" in data:
            #    print(f"Error message: {data['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


def btc_address(phrase):
    mnemon = Mnemonic('english')
    seed = mnemon.to_seed(phrase)
    #print(f'BIP39 Seed: {seed.hex()}\n')

    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    root_address = root_key.Address()
    root_public_hex = root_key.PublicKey().hex()
    root_private_wif = root_key.WalletImportFormat()
    #print('Root key:')
    #print(f'\tAddress: {root_address}')
    #print(f'\tPublic : {root_public_hex}')
    #print(f'\tPrivate: {root_private_wif}\n')

    child_key = root_key.ChildKey(0).ChildKey(0)
    child_address = child_key.Address()
    child_public_hex = child_key.PublicKey().hex()
    child_private_wif = child_key.WalletImportFormat()
    #print('Child key m/0/0:')
    #print(f'\tAddress: {child_address}')
    #print(f'\tPublic : {child_public_hex}')
    #print(f'\tPrivate: {child_private_wif}\n')
    return child_address


def check_address_transactions_btc(address_btc):
    api_url = f"https://blockstream.info/api/address/{address_btc}/txs"
    response = requests.get(api_url)
    transactions = response.json()
    
    if transactions:
        print(f"The address {address_btc} has had transactions.")
        print(phrase)
        new_data = {"phrase": phrase, "address": address_btc, "chain": "BTC"}
        append_to_json(file_path, new_data)
        #for transaction in transactions:
        #    txid = transaction['txid']
        #    print(f"- {txid}")
    else:
        pass
        #print(f"The address {address_btc} has no transactions.")



for i in range(100000):
    print("Loop iteration:", i)
    Account.enable_unaudited_hdwallet_features()
    acct, mnemonic = Account.create_with_mnemonic(num_words=24)
    address= acct.address
    phrase= mnemonic
    check_transactions(address)
    check_address_transactions(address)
    address_btc= btc_address(phrase)
    check_address_transactions_btc(address_btc)
