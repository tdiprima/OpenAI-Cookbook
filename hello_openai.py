import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Use the completions endpoint to generate a completion
response = client.completions.create(model="gpt-3.5-turbo-instruct",  prompt="Hello World!")

print(f"Completion: {response.choices[0].text}")
