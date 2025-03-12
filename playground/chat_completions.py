"""
Test chat completions with system and user, temperature and max tokens.
https://platform.openai.com/docs/quickstart?api-mode=chat
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(model="gpt-4",
messages=[
    {"role": "system", "content": "You are a helpful, witty, and friendly assistant."},
    {"role": "user", "content": "Can you explain quantum computing?"}
],
temperature=0.7,
max_tokens=150)

print(response.choices[0].message.content)
