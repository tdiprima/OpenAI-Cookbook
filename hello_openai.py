"""
Test OpenAI Key

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = 'tdiprima'
__version__ = '1.0'
__license__ = 'MIT'

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Use the completions endpoint to generate a completion
response = client.completions.create(model="gpt-3.5-turbo-instruct",  prompt="Hello! Who are you?")

print(f"Completion: {response.choices[0].text}")
