import base64, codecs, json, requests, os, hashlib, secrets, pprint
from termcolor import colored


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
url = f'https://{REST_HOST}/v1/payments'

response = requests.get(
    url,
    headers=headers,
    verify=TLS_PATH
)
# pprint.pprint(json.loads(response.content))
data = json.loads(response.content)
print(os.getenv("LND_DIR"))
for payment in data["payments"]:
    print(
        colored("Payment", "blue"),
        payment["status"],
        payment["creation_time_ns"],
        payment["payment_hash"],
        payment["value_msat"],
        len(payment["htlcs"])
    )