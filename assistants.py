import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Example Assistant Behavior
system_prompt = """
You are a financial advisor. Respond concisely and focus on investment strategies.
"""

# Test via Chat Completions
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What are the best stocks to invest in right now?"}
    ]
)
print(response['choices'][0]['message']['content'])
