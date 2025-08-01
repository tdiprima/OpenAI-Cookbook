"""
Retrieve a list of available models from the xAI API
https://docs.x.ai/docs/api-reference#list-models
Author: tdiprima
"""
import os
from datetime import datetime

import pytz
import requests

# Define California timezone
california_tz = pytz.timezone('America/Los_Angeles')

# Sort by name (True) or date (False) - default is date
SORT_BY_NAME = False

api_key = os.getenv("OPENAI_API_KEY")
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.get('https://api.openai.com/v1/models', headers=headers)

if response.status_code == 200:
    models = response.json()
    
    # Sort models based on the switch
    if SORT_BY_NAME:
        models['data'].sort(key=lambda x: x['id'])
    else:
        models['data'].sort(key=lambda x: x['created'])
    
    for model in models['data']:
        timestamp = model['created']
        # Convert UTC timestamp to local California time
        readable_date_local = datetime.fromtimestamp(timestamp, california_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"Model ID: {model['id']}, Created At: {readable_date_local}, Owned By: {model['owned_by']}")
else:
    print(f"Failed to retrieve models: {response.status_code} - {response.text}")
