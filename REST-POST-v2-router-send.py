import base64, codecs, json, requests, os, hashlib, secrets

# https://lightning.engineering/api-docs/api/lnd/router/send-payment-v2
# https://github.com/lightningnetwork/lnd/discussions/6357

def b64_hex_transform(plain_str: str) -> str:
    """Returns the b64 transformed version of a hex string"""
    a_string = bytes.fromhex(plain_str)
    return base64.b64encode(a_string).decode()


REST_HOST = 'localhost:8080'
MACAROON_PATH = os.getenv("LND_DIR") + '/data/chain/bitcoin/regtest/admin.macaroon'
TLS_PATH = os.getenv("LND_DIR") + '/tls.cert'

url = f'https://{REST_HOST}/v2/router/send'
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon, "Content-Type": "application/json"}

# A preimage is a 32-byte random value that will be used to generate the payment hash.
preimage = secrets.token_hex(32)
payment_hash = hashlib.sha256(bytes.fromhex(preimage))

dest = "02bad19b727facaad0f43b2dee4fd1e9cfe0c8c242d8f2b163237eced80ca9c643"

data = {
  'dest': b64_hex_transform(dest),
  'amt': 1000,
  'payment_hash': b64_hex_transform(payment_hash.hexdigest()),
  'timeout_seconds': 60,
  'fee_limit_sat': 10,
  'dest_custom_records': {
    5482373484: b64_hex_transform(preimage),
  },
}

r = requests.post(
    url,
    headers=headers,
    stream=True,
    data=json.dumps(data),
    verify=TLS_PATH
)

for raw_response in r.iter_lines():
  json_response = json.loads(raw_response)
  print(json_response)

# {
#    "payment_hash": <string>,
#    "value": <int64>,
#    "creation_date": <int64>,
#    "fee": <int64>,
#    "payment_preimage": <string>,
#    "value_sat": <int64>,
#    "value_msat": <int64>,
#    "payment_request": <string>,
#    "status": <PaymentStatus>,
#    "fee_sat": <int64>,
#    "fee_msat": <int64>,
#    "creation_time_ns": <int64>,
#    "htlcs": <HTLCAttempt>,
#    "payment_index": <uint64>,
#    "failure_reason": <PaymentFailureReason>,
# }