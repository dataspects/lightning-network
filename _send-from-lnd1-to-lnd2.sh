#!/bin/bash

source ~/.bash_aliases
shopt -s expand_aliases

export LND_DIR=$HOME/lightning-network-implementation/.lnd
export RECIPIENT_PORT=8080
export RECIPIENT_PUBKEY=$(lncli2 getinfo | jq -r .identity_pubkey)
export SATS_AMOUNT=10000

poetry run python3 REST-POST-v2-router-send.py