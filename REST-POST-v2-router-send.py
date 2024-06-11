import base64, codecs, json, requests, os, hashlib, secrets, pprint
from termcolor import colored

# https://lightning.engineering/api-docs/api/lnd/router/send-payment-v2
# https://github.com/lightningnetwork/lnd/discussions/6357

def b64_transform(plain_str: str) -> str:
    """Returns the b64 transformed version of a string"""
    return base64.b64encode(plain_str.encode()).decode()

def b64_hex_transform(plain_str: str) -> str:
    """Returns the b64 transformed version of a hex string"""
    a_string = bytes.fromhex(plain_str)
    return base64.b64encode(a_string).decode()

###

REST_HOST = 'localhost:' + str(os.getenv("RECIPIENT_PORT"))
MACAROON_PATH = os.getenv("LND_DIR") + '/data/chain/bitcoin/regtest/admin.macaroon'
TLS_PATH = os.getenv("LND_DIR") + '/tls.cert'

###

print("SATS:\t\t", os.getenv("SATS_AMOUNT"))
print("MESSAGE:\t", base64.b64decode(b64_transform(os.getenv("MESSAGE"))).decode('utf-8'))

url = f'https://{REST_HOST}/v2/router/send'
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon, "Content-Type": "application/json"}

# A preimage is a 32-byte random value that will be used to generate the payment hash.
preimage = secrets.token_hex(32)
payment_hash = hashlib.sha256(bytes.fromhex(preimage))

data = {
  'dest': b64_hex_transform(os.getenv("RECIPIENT_PUBKEY")),
  'amt': os.getenv("SATS_AMOUNT"),
  'payment_hash': b64_hex_transform(payment_hash.hexdigest()),
  'timeout_seconds': 60,
  'fee_limit_sat': 10,
  'dest_custom_records': {
    5482373484: b64_hex_transform(preimage),
    34349334: b64_transform(os.getenv("MESSAGE"))
  },
}

stream_of_payment_updates = requests.post(
    url,
    headers=headers,
    stream=True,
    data=json.dumps(data),
    verify=TLS_PATH
)

print(colored("Payment update stream:", "blue"))
for payment_update in stream_of_payment_updates.iter_lines():
  pur = json.loads(payment_update)["result"]
  print(pur["status"], ":\t", pur["failure_reason"])
  if pur["failure_reason"] in [
                                "FAILURE_REASON_NO_ROUTE",
                                "FAILURE_REASON_INSUFFICIENT_BALANCE"
                              ]:
     print(colored("Check channels and local_balance!", "red"), "(lncli* listchannels)")
     #QUESTION: 
     print(colored("Mine/confirm 200 blocks!", "red"), "(bitcoin-cli -generate 200)")



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