# lightning-network

## EXPLANATION: What is a Lightning network and how does it relate to Bitcoin?

The **lightning network** acts as the **tab running at a bar**. The tab is a **payment channel** between **you and the bar**.

When ordering the first drink, you provide a **credit card**, similar to **initiating a payment channel**. Then as the night proceeds, and you're having too much fun, you will order multiple drinks; these **multiple drink orders** are **recorded transactions**. While going through these drinks, you haven't technically spent any money on these drinks. It's only until the end of the night when you pay for the drinks by closing out your tab.

With the lightning network, **2 transactions happen on the Bitcoin network**:

1. **opening a payment channel** (starting the tab)
2. **closing a payment channel** (closing out the tab)

## SETUP

Based on https://www.bitstein.org/blog/setting-up-a-bitcoin-lightning-network-test-environment.

### DOWNLOAD/EXTRACT: Software

* **lnd-linux-amd64-v0.18.0-beta.tar.gz** (https://github.com/lightningnetwork/lnd/releases)
* **bitcoin-27.0-x86_64-linux-gnu.tar.gz** (https://bitcoincore.org/bin/bitcoin-core-27.0/)

These archives are expected to be unpacked at `$HOME/Downloads/` (hack).

### EDIT: $HOME/.bash_aliases

```bash
export BITCOIND_DIR="$HOME/lightning-network-implementation/.bitcoin"

alias bitcoind="$HOME/Downloads/bitcoin-27.0-x86_64-linux-gnu/bitcoin-27.0/bin/bitcoind -datadir=$BITCOIND_DIR -fallbackfee=0.0002"
alias bitcoin-cli="$HOME/Downloads/bitcoin-27.0-x86_64-linux-gnu/bitcoin-27.0/bin/bitcoin-cli -datadir=$BITCOIND_DIR"

export LND1_DIR="$HOME/lightning-network-implementation/.lnd1"
export LND2_DIR="$HOME/lightning-network-implementation/.lnd2"

alias lnd1="$HOME/Downloads/lnd-linux-amd64-v0.18.0-beta/lnd --lnddir=$LND1_DIR";
alias lncli1="$HOME/Downloads/lnd-linux-amd64-v0.18.0-beta/lncli -n regtest --lnddir=$LND1_DIR"

alias lnd2="$HOME/Downloads/lnd-linux-amd64-v0.18.0-beta/lnd --lnddir=$LND2_DIR";
alias lncli2="$HOME/Downloads/lnd-linux-amd64-v0.18.0-beta/lncli -n regtest --lnddir=$LND2_DIR --rpcserver=localhost:11009"
```

| FYI: Some important commands                   | Comments                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| `bitcoind`                                     | Start (Might require `bitcoin-cli createwallet testwallet` first.) |
| `bitcoin-cli stop`                             |                                                                    |
| `bitcoin-cli createwallet testwallet`          |                                                                    |
| `bitcoin-cli listwallets`                      |                                                                    |
| `bitcoin-cli loadwallet testwallet`            |                                                                    |
| `bitcoin-cli -generate 101`                    | Generate 101 blocks                                                |
| `bitcoin-cli -rpcwallet=testwallet getbalance` |                                                                    |

### EDIT: $HOME/lightning-network-implementation/.bitcoin/bitcoin.conf

Create `rpcuser` and `rpcpassword` using https://github.com/bitcoin/bitcoin/tree/master/share/rpcauth.

```
regtest=1
daemon=1
txindex=1
rpcuser=
rpcpassword=
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28333
```

### EDIT: $HOME/lightning-network-implementation/.lnd1/lnd.conf

```
# https://docs.lightning.engineering/lightning-network-tools/lnd/lnd.conf

[Application Options]

restlisten=8080
accept-amp=true
accept-keysend=true

[Bitcoin]

bitcoin.active=1
bitcoin.regtest=1
bitcoin.node=bitcoind

[Bitcoind]

bitcoind.rpchost=localhost
bitcoind.rpcuser=
bitcoind.rpcpass=
bitcoind.zmqpubrawblock=tcp://127.0.0.1:28332
bitcoind.zmqpubrawtx=tcp://127.0.0.1:28333
```

| FYI: Some important commands            | Comments                 |
| --------------------------------------- | ------------------------ |
| `lnd1`                                  | Start                    |
| `lncli1 state`                          |                          |
| `lncli1 create`                         |                          |
| `lncli1 getinfo`                        | Requires unlocked wallet |
| `lncli1 unlock`                         |                          |
| `lncli1 getinfo \| jq -r .identity_pubkey` |                          |
| `lncli1 walletbalance`                  |                          |

### EDIT: $HOME/lightning-network-implementation/.lnd2/lnd.conf

```
[Application Options]

listen=0.0.0.0:9734
rpclisten=localhost:11009
restlisten=0.0.0.0:8180
accept-amp=true
accept-keysend=true

[Bitcoin]

bitcoin.active=1
bitcoin.regtest=1
bitcoin.node=bitcoind

[Bitcoind]

bitcoind.rpchost=localhost
bitcoind.rpcuser=
bitcoind.rpcpass=
bitcoind.zmqpubrawblock=tcp://127.0.0.1:28332
bitcoind.zmqpubrawtx=tcp://127.0.0.1:28333
```

| FYI: Some important commands               | Comments                 |
| ------------------------------------------ | ------------------------ |
| `lnd2`                                     | Start                    |
| `lncli2 state`                             |                          |
| `lncli2 create`                            |                          |
| `lncli2 getinfo`                           | Requires unlocked wallet |
| `lncli2 unlock`                            |                          |
| `lncli2 getinfo \| jq -r .identity_pubkey` |                          |
| `lncli2 walletbalance`                     |                          |

### EXECUTE: setup nodes and connect lightning nodes

Create wallets on the bitcoin and the lightning nodes:

```bash
bitcoin-cli createwallet testwallet
...follow instructions

lncli1 create
...follow instructions

lncli2 create
...follow instructions
```

Connect lightning nodes

`lncli1 connect $(lncli2 getinfo | jq -r .identity_pubkey)@localhost:9734`

`lncli1 listpeers`

## EXAMPLE: send bitcoins from bitcoin node to lightning node 2 and create channel between lightning node 1 and lightning node 2

### MINE bitcoins

`bitcoin-cli -generate 5` (mine 5)

`bitcoin-cli -generate 101` (confirm)

### OBTAIN lightning node 2 address

`lncli2 newaddress np2wkh`

Copy **address**.

### SEND bitcoin to lightning node 2 address

`bitcoin-cli sendtoaddress <address> 1` (sending 1 bitcoin)

`bitcoin-cli -generate 6` (confirm)

### CREATE channel

Start channel from Lightning Network Daemon 1 to Lightning Network Daemon 2:

`lncli1 openchannel $(lncli2 getinfo | jq -r .identity_pubkey) 100000` (100'000 satoshis), this returns `funding_txid`

#UNDERSTAND: 1) lnd1 must have >= 100000 sats and 2) the channel opening must be confirmed by blocks mined on/by the bitcoin node 

`bitcoin-cli -generate 10`

### CHECK

`lncli1 listchannels`

### DEVELOPING: Keysend (under construction!)

https://docs.lightning.engineering/lightning-network-tools/lnd/send-messages-with-keysend

`lncli2 sendpayment --dest <destination public key> --amt 2 --keysend`

## START

| Bitcoin Core                                                         | Lightning Network Daemon 1 (lnd1)                 | Lightning Network Daemon 2 (lnd2)                 |
| -------------------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------- |
| Start<br/>`bitcoind`                                                 | Start<br/>`lnd1`                                  | Start<br/>`lnd2`                                  |
| `bitcoin-cli loadwallet testwallet`                                  | `lncli1 unlock` (wallet)                          | `lncli2 unlock` (wallet)                          |
| `bitcoin-cli -rpcwallet=testwallet getbalance`                       | `lncli1 walletbalance`                            | `lncli2 walletbalance`                            |
|                                                                      | `lncli1 listpeers`                                | `lncli2 listpeers`                                |
|                                                                      | `lncli1 getinfo \| jq -r .identity_pubkey` (ipk1) | `lncli2 getinfo \| jq -r .identity_pubkey` (ipk2) |
|                                                                      | `lncli1 connect <ipk2>@localhost:9734`            |                                                   |
| If `lncli1 connect` fails:<br/>`bitcoin-cli -generate 100` (or more) |                                                   |                                                   |
|                                                                      | `lncli1 listpeers`                                | `lncli2 listpeers`                                |
|                                                                      | `lncli1 listchannels`                             | `lncli2 listchannels`                             |

* `lncli1 connect $(lncli2 getinfo | jq -r .identity_pubkey)@localhost:9734`

## INSPECT: channels

```
lncli* listchannels | jq -c .channels[] | while read channel; do echo LIGHTNODE1_CHANNEL.remote_pubkey = $(echo $channel | jq -r .remote_pubkey) capacity=$(echo $channel | jq -r .capacity); done
```

## OPERATE: send payment between Lightning Network Daemons

### 1. `_check-system-as-seen-from-lnd1.sh`

* #LOOK-UP-DATA: `.local_balance` and `.remote_balance`

### 2. `./_send-from-lnd1-to-lnd2.sh`

### 3. `_check-system-as-seen-from-lnd1.sh`

* #EFFECT: `local_balance` should decrease and `remote_balance` should increase 

# TOOLS

* https://raspibolt.org/guide/bonus/bitcoin/mempool.html