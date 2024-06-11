#!/bin/bash

source ~/.bash_aliases
shopt -s expand_aliases

export LND_DIR=$HOME/lightning-network-implementation/.lnd2
export RECIPIENT_PORT=8180

poetry run python3 REST-GET-v1-payments.py