"""
Test chat completions with system and user, temperature and max tokens.
https://platform.openai.com/docs/quickstart?api-mode=chat
"""

import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """

"""

if PROMPT.strip():

    try:
        response = client.chat.completions.create(
            model="gpt-5.2",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful, witty, and friendly assistant.",
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
