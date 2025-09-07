"""
This script queries the assistant created, to search and retrieve information from the uploaded file.
Author: tdiprima
"""

import os

from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def query_assistant(assistant_id, query):
    # Create a thread with the user's query
    thread = client.beta.threads.create(messages=[{"role": "user", "content": query}])

    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant_id
    )

    # Wait for the run to complete
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run status: {run.status}")
        import time

        time.sleep(1)

    # Retrieve the assistant's response
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for message in messages.data:
            if message.role == "assistant":
                return message.content[0].text.value
    else:
        error_details = f"Run failed with status: {run.status}"
        if hasattr(run, "last_error") and run.last_error:
            error_details += f", Error: {run.last_error}"
        return error_details


def main():
    # Replace with your assistant ID from the first script
    assistant_id = "asst_xxxxxxxxxxxxxxxxxxxxxxxx"

    # Query the assistant
    # query = "Summarize the main points of the uploaded document."
    query = "What is deep research by OpenAI?"
    response = query_assistant(assistant_id, query)
    print(f"Assistant response: {response}")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    main()
