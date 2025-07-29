"""
Test chat completions with system and user, temperature and max tokens.
https://platform.openai.com/docs/quickstart?api-mode=chat
"""
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
Develop a type-safe agent with Python PydanticAI: Define a structured output model (e.g., `BaseModel` for news summaries) and build an agent that scrapes articles, validates outputs, and stores results in a database.
Then, write a README.md on how it works.  Give a summary of what it's doing, and then explain what the code is doing.
Generate a good folder name for this code.
"""

response = client.chat.completions.create(model="gpt-4.1",
messages=[
    {"role": "system", "content": "You are an expert in Agentic AI, and you are happy to share code, and info in easy-to-understand language."},
    {"role": "user", "content": PROMPT}
],
temperature=0.5)

print(response.choices[0].message.content)
