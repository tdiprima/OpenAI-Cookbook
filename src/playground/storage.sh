#!/bin/bash
#
# Author: tdiprima
# Date: 2024-11-21
# Description: Script for managing file uploads with OpenAI API
# - Uploads a JSONL file to OpenAI
# - Lists all uploaded files
#
# Usage: Modify "path/to/file.jsonl" with the actual file path before running.
# https://platform.openai.com/storage/
#

# Upload
openai api files.upload -p "path/to/file.jsonl"

# List files
openai api files.list
