"""
Web Search
An agent that searches the web for the latest AI news
"""
import openai

# Init the client
client = openai.OpenAI()

# Ask for the latest scoop
response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    input="What's the latest breakthrough in AI as of March 19, 2025?"
)

# Show off the results 🎉
print("Answer:", response.output_text)
if hasattr(response, "citations"):  # Check for sources
    print("Sources:", response.citations)
