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
                    # "content": "You are a helpful, witty, and friendly assistant.",
                    "content": "You are an experienced Red Teamer who is happy to share knowledge."
                },
                {"role": "user", "content": PROMPT},
            ],
            temperature=0.7,
        )

        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Error: {e}")
else:
    print("Please add a prompt to the PROMPT variable before running.")
