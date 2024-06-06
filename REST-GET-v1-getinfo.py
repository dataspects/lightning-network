import base64, codecs, json, requests, os

# https://lightning.engineering/api-docs/api/lnd/lightning/get-info

REST_HOST = 'localhost:8080'
MACAROON_PATH = os.getenv("LND_DIR") + '/data/chain/bitcoin/regtest/admin.macaroon'
TLS_PATH = os.getenv("LND_DIR") + '/tls.cert'

url = f'https://{REST_HOST}/v1/getinfo'
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon}
r = requests.get(url, headers=headers, verify=TLS_PATH)
print(r.json())

# {
#    "version": <string>,
#    "commit_hash": <string>,
#    "identity_pubkey": <string>,
#    "alias": <string>,
#    "color": <string>,
#    "num_pending_channels": <uint32>,
#    "num_active_channels": <uint32>,
#    "num_inactive_channels": <uint32>,
#    "num_peers": <uint32>,
#    "block_height": <uint32>,
#    "block_hash": <string>,
#    "best_header_timestamp": <int64>,
#    "synced_to_chain": <bool>,
#    "synced_to_graph": <bool>,
#    "testnet": <bool>,
#    "chains": <Chain>,
#    "uris": <string>,
#    "features": <FeaturesEntry>,
#    "require_htlc_interceptor": <bool>,
#    "store_final_htlc_resolutions": <bool>,
# }