from openai import OpenAI


# Initialize the OpenAI client
client = OpenAI()

# Fetch the list of available models
models = client.models.list()

# Print the model IDs
for model in models.data:
    print(model.id)
