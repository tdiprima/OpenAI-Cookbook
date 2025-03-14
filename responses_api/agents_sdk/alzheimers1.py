"""
Using the OpenAI Python library (not openai-agents) with the Assistants API to
create a research assistant that fetches and summarizes papers from ArXiv.
Author: tdiprima
"""
import asyncio
import openai
from openai import AsyncOpenAI
import arxiv
from arxiv import Client
import os

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to fetch research papers from Arxiv (synchronous, but called within async context)
def fetch_research_papers(topic):
    search = arxiv.Search(
        query=topic,
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in Client().results(search):
        papers.append({
            "title": result.title,
            "abstract": result.summary,
            "url": result.entry_id
        })
    return papers


# Async main function
async def main():
    # Initialize the async client
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Create the Assistant
    assistant = await client.beta.assistants.create(
        model="gpt-4",
        name="Medical Research Assistant",
        instructions="You are a research assistant specializing in summarizing medical papers. Given a research topic, "
                     "find the latest papers and summarize their key findings.",
        tools=[{
            "type": "function",
            "function": {
                "name": "fetch_research_papers",
                "description": "Fetches recent research papers on a given medical topic from Arxiv",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The research topic to search for papers about"
                        }
                    },
                    "required": ["topic"]
                }
            }
        }]
    )

    # Query the Assistant
    query = "Latest research on Alzheimer's treatment"
    thread = await client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": query
        }]
    )

    # Create the run
    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    # Poll the run status asynchronously
    while True:
        run_status = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        if run_status.status == "completed":
            # Fetch the messages from the thread
            messages = await client.beta.threads.messages.list(thread_id=thread.id)
            # Print the assistant's final response
            for message in messages.data:
                if message.role == "assistant":
                    print("Assistant Response:")
                    print(message.content[0].text.value)
            break

        elif run_status.status == "requires_action":
            # Handle tool calls
            tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                if tool_call.function.name == "fetch_research_papers":
                    # Parse the arguments
                    arguments = eval(tool_call.function.arguments)  # Convert string to dict
                    topic = arguments["topic"]
                    # Execute the synchronous function (in async context)
                    papers = fetch_research_papers(topic)
                    # Prepare the output
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": str(papers)  # Convert to string for submission
                    })

            # Submit the tool outputs back to the run
            await client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        # Wait briefly before checking again (non-blocking in async context)
        await asyncio.sleep(1)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
