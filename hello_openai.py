import os
import openai

# My personal API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use the completions endpoint to generate a completion
response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",  # text-davinci-003
    prompt="Hello World!"
)

print(f"Completion: {response['choices'][0]['text']}")
