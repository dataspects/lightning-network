#!/bin/bash

echo "Development and Understanding Dashboard"

clear; egrep \
  --line-number --recursive --color=always \
  --context=0 \
  --include \*.sh \
  --include \*.py \
  --include \*.md \
  --exclude \*.lock \
  --exclude \*.toml \
  --exclude development-and-understanding-dashboard.sh \
  "#QUESTION|#UNDERSTAND|#EFFECT"