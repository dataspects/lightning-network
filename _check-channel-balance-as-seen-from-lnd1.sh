#!/bin/bash

source ~/.bash_aliases
shopt -s expand_aliases

export LND_DIR=$HOME/lightning-network-implementation/.lnd
export RECIPIENT_PORT=8080

poetry run python3 REST-GET-v1-balance-channels.py