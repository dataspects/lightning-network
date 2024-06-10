#!/bin/bash

source ~/.bash_aliases
shopt -s expand_aliases

export LND_DIR=$HOME/lightning-network-implementation/.lnd2
export RECIPIENT_PORT=8180
export RECIPIENT_PUBKEY=$(lncli1 getinfo | jq -r .identity_pubkey)
export SATS_AMOUNT=10000

poetry run python3 REST-POST-v2-router-send.py
