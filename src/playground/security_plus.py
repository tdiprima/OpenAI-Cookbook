# =============================================================================
# CompTIA Security+ Study Assistant
# -----------------------------------------------------------------------------
# Uses the OpenAI API to generate beginner-friendly explanations of Security+
# topics, tailored for ADHD learners via storytelling, patterns, and hands-on
# framing. Edit the PROMPT variable to explore different exam domains.
# =============================================================================
import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
I'm looking to take the 'CompTIA Security+' certification.
I'm a beginner who's looking to understand some things up front.

Teach me about:
The Fundamentals of Security

With ADHD, my brain tends to remember:
- interesting things
- emotionally charged things
- hands-on things
- stories
- patterns
So use those ideas when teaching me these concepts.

In 500 words or less.

I already know that using certain commands & tools on networks you do not own or have permission to test can get you in trouble.
So don't mention it.

Don't make any further recommendations at the end.
"""

if PROMPT.strip():

    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
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
