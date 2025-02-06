"""
Programmatically Adjusting Message History to Manage Token Limits

In a chatbot application, you might want to:
Maintain a "summary" of the conversation for context.
Remove old messages when the token count grows too high.

Author: tdiprima
Version: 1.0
License: MIT
"""

__author__ = 'tdiprima'
__version__ = '1.0'
__license__ = 'MIT'

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to truncate messages
def truncate_messages(messages, max_input_tokens=3000):
    """Truncate message history to fit within the input token limit."""
    total_tokens = sum(len(message['content']) for message in messages)
    while total_tokens > max_input_tokens:
        messages.pop(0)  # Remove oldest message
        total_tokens = sum(len(message['content']) for message in messages)
    return messages


# Initialize conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def chat_with_gpt(user_input, max_output_tokens=150):
    global messages

    # Add user input to messages
    messages.append({"role": "user", "content": user_input})

    # Truncate messages if needed
    messages = truncate_messages(messages)

    # Call OpenAI API
    response = client.chat.completions.create(model="gpt-4",
    messages=messages,
    temperature=0.7,
    max_tokens=max_output_tokens)  # Dynamically allocate output tokens

    # Get assistant's response
    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message


# Example conversation
# print(chat_with_gpt("Hello! Can you tell me about quantum computing?"))
# print(chat_with_gpt("What are some examples of its real-world applications?"))
print(chat_with_gpt("Hello! Can you explain quantum computing?", max_output_tokens=200))
print(chat_with_gpt("What are some real-world applications?", max_output_tokens=300))
