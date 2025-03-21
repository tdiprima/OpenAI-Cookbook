import openai

# Set up the client
client = openai.OpenAI()

# Upload a file (do this once—replace with your file path!)
with open("ai_trends_2025.pdf", "rb") as file:
    uploaded_file = client.files.create(file=file, purpose="search")

# Search that file with Responses API
response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "file_search", "file_ids": [uploaded_file.id]}],
    input="What's the top AI prediction for 2025 in this doc?"
)

# Reveal the treasure 🪙
print(response.output_text)
