#!/usr/bin/env bash
# Description: Get API models
# Author: tdiprima

curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
