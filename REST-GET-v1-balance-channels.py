import base64, codecs, json, requests, os, hashlib, secrets, pprint

RECIPIENT_PORT = 8180

###

def b64_hex_transform(plain_str: str) -> str:
    """Returns the b64 transformed version of a hex string"""
    a_string = bytes.fromhex(plain_str)
    return base64.b64encode(a_string).decode()

REST_HOST = 'localhost:' + str(os.getenv("RECIPIENT_PORT"))
MACAROON_PATH = os.getenv("LND_DIR") + '/data/chain/bitcoin/regtest/admin.macaroon'
TLS_PATH = os.getenv("LND_DIR") + '/tls.cert'

macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon, "Content-Type": "application/json"}

# Fetch and print the channel balances
balance_url = f'https://{REST_HOST}/v1/balance/channels'

balance_response = requests.get(
    balance_url,
    headers=headers,
    verify=TLS_PATH
)

balance_data = balance_response.json()
print("Channel balances:")
pprint.pprint(balance_data)