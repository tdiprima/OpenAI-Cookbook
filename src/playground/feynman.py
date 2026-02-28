"""
Test chat completions with system and user, temperature and max tokens.
https://platform.openai.com/docs/quickstart?api-mode=chat
"""

import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
Teach me what BLAH is in machine learning, and why it's good for BLAH.
"""

if PROMPT.strip():

    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful, witty, and friendly assistant.  You teach using the Feynman and Gallo principles:
                    - Write the idea.
- Explain to a smart 12-year-old, no fancy words.  (But don't say '12-year-old').
- Use simple stories.
- Stories with villains, like zombie viruses attacking body castles.
- Great lessons have "holy smokes" shocks, and "ah-ha" moments.
- Make it stupidly simple for a dummy with ADHD to understand.
- Don't assume that I understand jargon or machine learning.
- Keep it simple; don't ramble on and on.
                    """,
                },
                {"role": "user", "content": PROMPT},
            ],
            temperature=1,
        )  # Default temperature GPT-5

        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Error: {e}")
else:
    print("Please add a prompt to the PROMPT variable before running.")
