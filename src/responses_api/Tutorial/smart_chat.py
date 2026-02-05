"""
Responses API Script
It's your AI's smart convo starter
An agent that answers a question using the Responses API
"""

import openai

# Set up your OpenAI client
client = openai.OpenAI()

# Fire off a question to the Responses API
response = client.responses.create(
    model="gpt-5.2",
    tools=[{"type": "web_search_preview"}],  # Tool to fetch web info
    input="What's the weather like in New York City today?",  # Your question
)

# Print the magic ✨
print(response.output_text)
