"""
This script uploads a file to OpenAI, creates an assistant with file search capabilities, and prepares it for queries.
https://platform.openai.com/docs/guides/tools-file-search is wrong.
Author: tdiprima
"""

import os

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Step 1: Upload a file to OpenAI
def upload_file(file_path):
    with open(file_path, "rb") as file:
        response = client.files.create(file=file, purpose="assistants")
    print(f"File upload response: {response}")
    return response.id


# Step 2: Create a vector store and attach the file
def create_vector_store(file_id):
    vector_store = client.beta.vector_stores.create(
        name="File Search Vector Store", file_ids=[file_id]
    )
    print(f"Vector store created: {vector_store.id}")
    return vector_store.id


# Step 3: Create an assistant with the file search tool linked to the vector store
def create_assistant(vector_store_id):
    assistant = client.beta.assistants.create(
        name="File Search Assistant",
        instructions="You are an assistant that helps users search and summarize content from uploaded files.",
        model="gpt-4-turbo-preview",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [
                    vector_store_id
                ]  # Use vector_store_ids, not file_ids
            }
        },
    )
    print(f"Assistant created with vector store: {assistant.id}")
    return assistant.id


def main():
    file_path = "deep_research_blog.pdf"

    # Upload the file
    file_id = upload_file(file_path)
    print(f"Uploaded file ID: {file_id}")

    # Create a vector store with the file
    vector_store_id = create_vector_store(file_id)

    # Create the assistant linked to the vector store
    assistant_id = create_assistant(vector_store_id)
    print(f"Final assistant ID: {assistant_id}")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    main()
