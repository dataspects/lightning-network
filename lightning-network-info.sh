#!/bin/bash

shopt -s expand_aliases
source $HOME/.bash_aliases

echo bitcoin-cli listwallets
echo BITCOIN_WALLETS = `bitcoin-cli listwallets`

echo bitcoin-cli -rpcwallet=testwallet getbalance
echo BALANCE = `bitcoin-cli -rpcwallet=testwallet getbalance` bitcoins

echo

echo lncli* getinfo
echo LIGHTNODE1_PUBKEY = `lncli1 getinfo | jq -r .identity_pubkey`
echo LIGHTNODE2_PUBKEY = `lncli2 getinfo | jq -r .identity_pubkey`

echo

echo lncli* walletbalance
echo LIGHTNODE1_WALLET.total_balance = `lncli1 walletbalance | jq -r .total_balance`
echo LIGHTNODE2_WALLET.total_balance = `lncli2 walletbalance | jq -r .total_balance`

echo
echo lncli* listchannels
lncli1 listchannels | jq -c .channels[] | while read channel; do echo LIGHTNODE1_CHANNEL.remote_pubkey = $(echo $channel | jq -r .remote_pubkey); done
lncli2 listchannels | jq -c .channels[] | while read channel; do echo LIGHTNODE2_CHANNEL.remote_pubkey = $(echo $channel | jq -r .remote_pubkey); done

