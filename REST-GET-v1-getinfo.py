import base64, codecs, json, requests, os, pprint
from termcolor import colored

# https://lightning.engineering/api-docs/api/lnd/lightning/get-info

REST_HOST = 'localhost:' + str(os.getenv("RECIPIENT_PORT"))
MACAROON_PATH = os.getenv("LND_DIR") + '/data/chain/bitcoin/regtest/admin.macaroon'
TLS_PATH = os.getenv("LND_DIR") + '/tls.cert'

url = f'https://{REST_HOST}/v1/getinfo'
macaroon = codecs.encode(open(MACAROON_PATH, 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon}
get_info = requests.get(url, headers=headers, verify=TLS_PATH).json()

# pprint.pprint(get_info)
print(colored("Get info for", "blue", attrs=["bold"]), os.getenv("LND_DIR"))
print(
    "synced_to_chain:", get_info["synced_to_chain"],
    "\nsynced_to_graph:", get_info["synced_to_graph"],
    "\nnum_active_channels", get_info["num_active_channels"],
    "\nnum_peers", get_info["num_peers"],
    "\nidentity_pubkey", get_info["identity_pubkey"],
    "\nblock_height", get_info["block_height"]
)

# LND_DIR=$HOME/lightning-network-implementation/.lnd1 poetry run python3 REST-GET-v1-getinfo.py

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