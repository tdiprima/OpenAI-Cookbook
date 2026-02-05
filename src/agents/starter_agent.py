"""
Classifies your input into "question" or "request"
Handles it differently based on what it thinks it is
Self-manages with just two API calls
"""

import os

from openai import OpenAI

# 1. Set up your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 2. Define a simple function to call the model
def call_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-5.2",  # or gpt-3.5-turbo if you want cheap
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# 3. Agent behavior
def starter_agent(user_input):
    # Step 1: Understand what the user wants
    task = call_llm(
        f"Classify this input: '{user_input}' into 'question', 'request', or 'other'."
    )

    # Step 2: Decide what to do
    if "question" in task.lower():
        answer = call_llm(f"Answer this question: {user_input}")
        return f"🔎 Here's your answer:\n{answer}"
    elif "request" in task.lower():
        action = call_llm(f"Explain how you would fulfill this request: {user_input}")
        return f"✅ Here's what I would do:\n{action}"
    return "🤷 Sorry, I didn't understand that. Can you rephrase?"


# 4. Run it
if __name__ == "__main__":
    user_input = input("🧠 What do you want the agent to do? ")
    result = starter_agent(user_input)
    print(result)
